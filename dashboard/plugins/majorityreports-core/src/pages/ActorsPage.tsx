import React from 'react';
import useAsync from 'react-use/lib/useAsync';
import {
  Page,
  Header,
  Content,
  Progress,
  ResponseErrorPanel,
  Select,
  SelectItem,
  SelectedItems,
  Table,
  TableColumn,
  Link,
} from '@backstage/core-components';

import Box from '@material-ui/core/Box';

import { Actor, ActorsResult } from '@internal/backstage-plugin-majorityreports-common';

import { FilterLayout } from '../components/FilterLayout';
import { usePage } from '../hooks/usePage';
import { usePageSize } from '../hooks/usePageSize';

const columns: TableColumn<Actor>[] = [
  {
    title: 'Name',
    field: 'name',
    highlight: true,
    render: (data) => <Link to={data.name}>{data.name}</Link>
  },
  {
    title: 'Namespace',
    field: 'namespace_name',
    render: (data) => <Link to={"../namespaces/" + data.namespace_name}>{data.namespace_name}</Link>
  },
  {
    title: 'Created',
    field: 'creationTimestamp',
    type: 'datetime',
  },
];

export const Filter = () => {
  const items: SelectItem[] = [];
  const [selected, setSelected] = React.useState<SelectedItems>();

  return (
    <Box pb={1} pt={1}>
      <Select
        label="Type"
        items={items}
        selected={selected}
        onChange={setSelected}
      />
    </Box>
  );
}

export const TableContent = () => {
  const [page, setPage] = usePage();
  const [pageSize, setPageSize] = usePageSize();

  const { value, loading, error } = useAsync(async (): Promise<ActorsResult> => {
    const proxyUrl = 'http://localhost:7007/api/proxy/api/';
    const url = new URL('api/actors', proxyUrl);
    url.searchParams.set('offset', (page * pageSize).toString());
    url.searchParams.set('limit', pageSize.toString());    
    return fetch(url.toString()).then((response) => response.json());
  }, [page, pageSize]);

  if (loading) {
    return <Progress />;
  } else if (error) {
    return <ResponseErrorPanel error={error} />;
  }

  return (
    <Table
      columns={columns}
      isLoading={loading}
      data={value?.items || []}
      page={page}
      options={{ pageSize }}
      onPageChange={setPage}
      onRowsPerPageChange={setPageSize}
      totalCount={value?.count || 0}
    />
  );
};

export const ActorsPage = () => (
  <Page themeId="actors">
    <Header title="Actors" />
    <Content>
      {/* <ContentHeader title="">
        <CreateButton title="Create" to="create" />
      </ContentHeader> */}
      <FilterLayout>
        <FilterLayout.Filter>
          <Filter />
        </FilterLayout.Filter>
        <FilterLayout.Content>
          <TableContent />
        </FilterLayout.Content>
      </FilterLayout>
    </Content>
  </Page>
);
