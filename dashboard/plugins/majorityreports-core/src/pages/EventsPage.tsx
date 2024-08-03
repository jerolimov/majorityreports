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
      options={{ paging: true }}
      columns={columns}
      data={data}
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
