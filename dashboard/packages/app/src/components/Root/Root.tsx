import React, { PropsWithChildren } from 'react';

import { SidebarPage } from '@backstage/core-components';

import { AppBar } from './AppBar';
import { Sidebar } from './Sidebar';

export const Root = ({ children }: PropsWithChildren<{}>) => {
  return (
    <>
      <AppBar />
      <SidebarPage>
        <Sidebar />
        {children}
      </SidebarPage>
    </>
  );
};
