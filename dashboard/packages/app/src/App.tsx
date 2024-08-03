import React from 'react';
import { Route, Navigate } from 'react-router-dom';
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
import {
  NamespacesPage,
  ActorsPage,
  ItemsPage,
  EventsPage,
  FeedbacksPage
} from '@internal/backstage-plugin-majorityreports-core';

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
    <Route path="/" element={<Navigate to="namespaces" />} />

    <Route path="/namespaces" element={<NamespacesPage />} />
    <Route path="/actors" element={<ActorsPage />} />
    <Route path="/items" element={<ItemsPage />} />
    <Route path="/events" element={<EventsPage />} />
    <Route path="/feedbacks" element={<FeedbacksPage />} />

    <Route path="/settings" element={<UserSettingsPage />} />
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
