import React from 'react';
import {
  Page,
  Header,
  Content,
  ResponseErrorPanel,
  Select,
  SelectItem,
  SelectedItems,
  Table,
  TableColumn,
  Link,
} from '@backstage/core-components';

import Box from '@material-ui/core/Box';

import { Namespace, NamespaceList } from '@internal/backstage-plugin-majorityreports-common';

import { useQuery } from '@tanstack/react-query';

import { FilterLayout } from '../components/FilterLayout';
import { Tags } from '../components/Tags';
import { usePage } from '../hooks/usePage';
import { usePageSize } from '../hooks/usePageSize';
import { formatCreationTimestamp } from '../utils/date';

const columns: TableColumn<Namespace>[] = [
  {
    title: 'Name',
    field: 'meta.name',
    highlight: true,
    render: (data) => <Link to={data.meta.name!}>{data.meta.name}</Link>
  },
  {
    title: 'Title',
    field: 'meta.title',
  },
  {
    title: 'Lifecycle',
    field: 'spec.lifecycle',
  },
  {
    title: 'Owner',
    field: 'spec.owner',
  },
  {
    title: 'Tags',
    field: 'meta.tags',
    render: (data) => <Tags object={data} />,
    sorting: false,
  },
  {
    title: 'Created',
    field: 'meta.creationTimestamp',
    type: 'datetime',
    render: formatCreationTimestamp,
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

  const result = useQuery<NamespaceList>({
    queryKey: ['namespaces', page, pageSize],
    queryFn: async function getNamespaces() {
      const proxyUrl = 'http://localhost:7007/api/proxy/api/';
      const path = 'api/namespaces';
      const url = new URL(path, proxyUrl);
      url.searchParams.set('start', (page * pageSize).toString());
      url.searchParams.set('limit', pageSize.toString());    
      const response = await fetch(url.toString());
      if (!response.ok) {
        throw new Error(`Failed to fetch namespaces, ${response.status} ${response.statusText}`);
      }
      return response.json();
    },
  });

  if (result.error) {
    return <ResponseErrorPanel error={result.error} />;
  }

  return (
    <Table
      columns={columns}
      isLoading={result.isLoading}
      data={result.data?.items || []}
      page={page}
      options={{ pageSize }}
      onPageChange={setPage}
      onRowsPerPageChange={setPageSize}
      totalCount={result.data?.meta.itemCount || 0}
    />
  );
};

export const NamespacesPage = () => (
  <Page themeId="namespaces">
    <Header title="Namespaces" type="Namespace" />
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
