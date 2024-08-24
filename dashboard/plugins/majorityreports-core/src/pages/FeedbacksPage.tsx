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

import { Feedback, FeedbackList } from '@internal/backstage-plugin-majorityreports-common';

import { useQuery } from '@tanstack/react-query';

import { FilterLayout } from '../components/FilterLayout';
import { Tags } from '../components/Tags';
import { usePage } from '../hooks/usePage';
import { usePageSize } from '../hooks/usePageSize';
import { useNamespace } from '../../../../packages/app/src/hooks/useNamespace';

const columns: TableColumn<Feedback>[] = [
  {
    title: 'Name',
    field: 'meta.name',
    highlight: true,
    render: (data) => <Link to={`/namespaces/${data.meta.namespace!}/feedbacks/${data.meta.name!}`}>{data.meta.name}</Link>
  },
  {
    title: 'Namespace',
    field: 'meta.namespace',
    render: (data) => <Link to={`/namespaces/${data.meta.namespace!}`}>{data.meta.namespace}</Link>
  },
  {
    title: 'Title',
    field: 'meta.title',
  },
  {
    title: 'Type',
    field: 'spec.type',
  },
  {
    title: 'Actor',
    field: 'spec.actor',
  },
  {
    title: 'Item',
    field: 'spec.item',
  },
  {
    title: 'Tags',
    field: 'meta.tags',
    render: (data) => <Tags object={data} />,
  },
  {
    title: 'Created',
    field: 'meta.creationTimestamp',
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
  const [namespace] = useNamespace();
  const filteredColumns = React.useMemo(() => namespace ? columns.filter((c) => c.field !== 'meta.namespace') : columns, [namespace]);
  const [page, setPage] = usePage();
  const [pageSize, setPageSize] = usePageSize();

  const result = useQuery<FeedbackList>({
    queryKey: ['feedbacks', namespace, page, pageSize],
    queryFn: async function getNamespaces() {
      const proxyUrl = 'http://localhost:7007/api/proxy/api/';
      const path = namespace ? `api/namespaces/${namespace}/feedbacks` : 'api/feedbacks';
      const url = new URL(path, proxyUrl);
      url.searchParams.set('start', (page * pageSize).toString());
      url.searchParams.set('limit', pageSize.toString());    
      const response = await fetch(url.toString());
      if (!response.ok) {
        throw new Error(`Failed to fetch feedbacks, ${response.status} ${response.statusText}`);
      }
      return response.json();
    },
  });

  if (result.error) {
    return <ResponseErrorPanel error={result.error} />;
  }

  return (
    <Table
      columns={filteredColumns}
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

export const FeedbacksPage = () => (
  <Page themeId="feedbacks">
    <Header title="Feedbacks" />
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
