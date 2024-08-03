import React from 'react';
import useAsync from 'react-use/lib/useAsync';
import {
  Page,
  Header,
  Content,
  Progress,
  ResponseErrorPanel,
  Table,
  TableColumn,
  useQueryParamState,
} from '@backstage/core-components';

type Event = {
  namespace_name: string;
  name: string;
  uid: string;
  creationTimestamp: string;
  updateTimestamp: string;
  labels: Record<string, string>;
  annotations: Record<string, string>;
};

const columns: TableColumn[] = [
  { title: 'Name', field: 'name' },
  { title: 'Namespace', field: 'namespace_name' },
  { title: 'Created', field: 'creationTimestamp', type: 'datetime' },
];

export const TableContent = () => {
  const [page, setPage] = useQueryParamState<number>('page');

  const { value: data, loading, error } = useAsync(async (): Promise<Event[]> => {
    return fetch('http://localhost:7007/api/proxy/api/api/events').then((response) => response.json());
  }, []);

  if (loading || !data) {
    return <Progress />;
  } else if (error) {
    return <ResponseErrorPanel error={error} />;
  }

  return (
    <Table
      columns={columns}
      isLoading={loading}
      data={data}
      page={page ?? 0}
      onPageChange={(changedPage, _changedPageSize) => setPage(changedPage)}
      totalCount={1000}
    />
  );
};

export const EventsPage = () => (
  <Page themeId="events">
    <Header title="Events" />
    <Content>
      <TableContent />
    </Content>
  </Page>
);
