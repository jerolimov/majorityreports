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

import { NamespacesResult } from '@internal/backstage-plugin-majorityreports-common';

import { usePage } from '../hooks/usePage';
import { usePageSize } from '../hooks/usePageSize';

const columns: TableColumn[] = [
  { title: 'Name', field: 'name' },
  { title: 'Created', field: 'creationTimestamp', type: 'datetime' },
];

export const TableContent = () => {
  const [page, setPage] = usePage();
  const [pageSize, setPageSize] = usePageSize();

  const { value, loading, error } = useAsync(async (): Promise<NamespacesResult> => {
    const proxyUrl = 'http://localhost:7007/api/proxy/api/';
    const url = new URL('api/namespaces', proxyUrl);
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

export const NamespacesPage = () => (
  <Page themeId="namespaces">
    <Header title="Namespaces" />
    <Content>
      <TableContent />
    </Content>
  </Page>
);
