import React from 'react';
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

import { Event, EventsResult } from '@internal/backstage-plugin-majorityreports-common';

import { useQuery } from '@tanstack/react-query';

import { FilterLayout } from '../components/FilterLayout';
import { Tags } from '../components/Tags';
import { usePage } from '../hooks/usePage';
import { usePageSize } from '../hooks/usePageSize';

const columns: TableColumn<Event>[] = [
  {
    title: 'Name',
    field: 'name',
    highlight: true,
    render: (data) => <Link to={`/namespaces/${data.namespace_name}/events/${data.name}`}>{data.name}</Link>
  },
  {
    title: 'Namespace',
    field: 'namespace_name',
    render: (data) => <Link to={`/namespaces/${data.namespace_name}`}>{data.namespace_name}</Link>
  },
  {
    title: 'Tags',
    render: (data) => <Tags object={data} />,
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

  const result = useQuery<EventsResult>({
    queryKey: ['events', page, pageSize],
    queryFn: function getNamespaces() {
      const proxyUrl = 'http://localhost:7007/api/proxy/api/';
      const url = new URL('api/events', proxyUrl);
      url.searchParams.set('offset', (page * pageSize).toString());
      url.searchParams.set('limit', pageSize.toString());    
      return fetch(url.toString()).then((response) => response.json());
    },
  });

  if (result.isLoading) {
    return <Progress />;
  } else if (result.error) {
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
      totalCount={result.data?.count || 0}
    />
  );
};

export const EventsPage = () => (
  <Page themeId="events">
    <Header title="Events" />
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
