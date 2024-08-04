import React from 'react';
import { useQueryParamState } from '@backstage/core-components';

export function usePageSize(): [number, (newPageSize: number) => void] {
  const [pageSizeParam, setPageSizeParam] = useQueryParamState<string>('pageSize');
  let pageSize = pageSizeParam ? parseInt(pageSizeParam) : 5;
  if (isNaN(pageSize)) pageSize = 5;
  const setPageSize = React.useCallback((newPageSize: number) => {
    if (pageSize !== newPageSize) {
      setPageSizeParam(newPageSize.toString());
    }
  }, []);
  return [pageSize, setPageSize];
}
