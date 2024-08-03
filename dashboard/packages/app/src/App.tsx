import React from 'react';
import { Route } from 'react-router-dom';
import { UserSettingsPage } from '@backstage/plugin-user-settings';
import { apis } from './apis';
import { Root } from './components/Root';

import {
  AlertDisplay,
  OAuthRequestDialog,
  SignInPage,
} from '@backstage/core-components';
import { createApp } from '@backstage/app-defaults';
import { AppRouter, FlatRoutes } from '@backstage/core-app-api';
import { MajorityreportsCorePage } from '@internal/backstage-plugin-majorityreports-core';

const app = createApp({
  apis,
  // bindRoutes({ bind }) {
  // },
  components: {
    SignInPage: props => <SignInPage {...props} auto providers={['guest']} />,
  },
});

const routes = (
  <FlatRoutes>
    {/* <Route path="/" element={<Navigate to="catalog" />} /> */}
    <Route path="/settings" element={<UserSettingsPage />} />
    <Route path="/majorityreports-core" element={<MajorityreportsCorePage />} />
  </FlatRoutes>
);

export default app.createRoot(
  <>
    <AlertDisplay />
    <OAuthRequestDialog />
    <AppRouter>
      <Root>{routes}</Root>
    </AppRouter>
  </>,
);
