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

type Actor = {
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
  const { value: data, loading, error } = useAsync(async (): Promise<Actor[]> => {
    return fetch('http://localhost:7007/api/proxy/api/api/actors').then((response) => response.json());
  }, []);

  if (loading || !data) {
    return <Progress />;
  } else if (error) {
    return <ResponseErrorPanel error={error} />;
  }

  return (
    <Table
      columns={columns}
      data={data}
    />
  );
};

export const ActorsPage = () => (
  <Page themeId="actors">
    <Header title="Actors" />
    <Content>
      <TableContent />
    </Content>
  </Page>
);
