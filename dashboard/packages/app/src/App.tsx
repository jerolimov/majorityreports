import React from 'react';
import { Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

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
  NamespaceDetailsPage,
  ActorsPage,
  ActorDetailsPage,
  ItemsPage,
  ItemDetailsPage,
  EventsPage,
  EventDetailsPage,
  FeedbacksPage,
  FeedbackDetailsPage,
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
    <Route path="/namespaces/:namespace_name" element={<NamespaceDetailsPage />} />

    <Route path="/actors" element={<ActorsPage />} />
    <Route path="/namespaces/:namespace_name/actors" element={<ActorsPage />} />
    <Route path="/namespaces/:namespace_name/actors/:actor_name" element={<ActorDetailsPage />} />

    <Route path="/items" element={<ItemsPage />} />
    <Route path="/namespaces/:namespace_name/items" element={<ItemsPage />} />
    <Route path="/namespaces/:namespace_name/items/:item_name" element={<ItemDetailsPage />} />

    <Route path="/events" element={<EventsPage />} />
    <Route path="/namespaces/:namespace_name/events" element={<EventsPage />} />
    <Route path="/namespaces/:namespace_name/events/:event_name" element={<EventDetailsPage />} />

    <Route path="/feedbacks" element={<FeedbacksPage />} />
    <Route path="/namespaces/:namespace_name/feedbacks" element={<FeedbacksPage />} />
    <Route path="/namespaces/:namespace_name/feedbacks/:feedback_name" element={<FeedbackDetailsPage />} />

    <Route path="/settings" element={<UserSettingsPage />} />
  </FlatRoutes>
);

const queryClient = new QueryClient();

export default app.createRoot(
  <>
    <AlertDisplay />
    <OAuthRequestDialog />
    <QueryClientProvider client={queryClient}>
      <AppRouter>
        <Root>{routes}</Root>
      </AppRouter>
    </QueryClientProvider>
  </>,
);
