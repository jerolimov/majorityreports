import React from 'react';
import { useQueryParamState } from '@backstage/core-components';

export function usePage(): [number, (newPage: number, newPageSize: number) => void] {
  const [pageParam, setPageParam] = useQueryParamState<string>('page');
  const [pageSizeParam, setPageSizeParam] = useQueryParamState<string>('pageSize');
  let page = pageParam ? parseInt(pageParam) : 0;
  if (isNaN(page)) page = 0;
  let pageSize = pageSizeParam ? parseInt(pageSizeParam) : 5;
  if (isNaN(pageSize)) pageSize = 5;
  const setPage = React.useCallback((newPage: number, newPageSize: number) => {
    if (page !== newPage) {
      setPageParam(newPage.toString());
    }
    if (pageSize !== newPageSize) {
      setPageSizeParam(newPageSize.toString());
    }
  }, []);
  return [page, setPage];
}
