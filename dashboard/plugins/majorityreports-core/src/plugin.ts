import {
  createPlugin,
  createRoutableExtension,
} from '@backstage/core-plugin-api';

import { rootRouteRef } from './routes';

export const plugin = createPlugin({
  id: 'majorityreports-core',
  routes: {
    root: rootRouteRef,
  },
});

export const NamespacesPage = plugin.provide(
  createRoutableExtension({
    name: 'MajorityReportsNamespacesPage',
    component: () => import('./pages/NamespacesPage').then(m => m.NamespacesPage),
    mountPoint: rootRouteRef,
  }),
);

export const NamespaceDetailsPage = plugin.provide(
  createRoutableExtension({
    name: 'MajorityReportsNamespaceDetailsPage',
    component: () => import('./pages/NamespaceDetailsPage').then(m => m.NamespaceDetailsPage),
    mountPoint: rootRouteRef,
  }),
);

export const ActorsPage = plugin.provide(
  createRoutableExtension({
    name: 'MajorityReportsActorsPage',
    component: () => import('./pages/ActorsPage').then(m => m.ActorsPage),
    mountPoint: rootRouteRef,
  }),
);

export const ActorDetailsPage = plugin.provide(
  createRoutableExtension({
    name: 'MajorityReportsActorDetailsPage',
    component: () => import('./pages/ActorDetailsPage').then(m => m.ActorDetailsPage),
    mountPoint: rootRouteRef,
  }),
);

export const ItemsPage = plugin.provide(
  createRoutableExtension({
    name: 'MajorityReportsItemsPage',
    component: () => import('./pages/ItemsPage').then(m => m.ItemsPage),
    mountPoint: rootRouteRef,
  }),
);

export const ItemDetailsPage = plugin.provide(
  createRoutableExtension({
    name: 'MajorityReportsItemsDetailsPage',
    component: () => import('./pages/ItemDetailsPage').then(m => m.ItemDetailsPage),
    mountPoint: rootRouteRef,
  }),
);

export const EventsPage = plugin.provide(
  createRoutableExtension({
    name: 'MajorityReportsEventsPage',
    component: () => import('./pages/EventsPage').then(m => m.EventsPage),
    mountPoint: rootRouteRef,
  }),
);

export const EventDetailsPage = plugin.provide(
  createRoutableExtension({
    name: 'MajorityReportsEventDetailsPage',
    component: () => import('./pages/EventDetailsPage').then(m => m.EventDetailsPage),
    mountPoint: rootRouteRef,
  }),
);

export const FeedbacksPage = plugin.provide(
  createRoutableExtension({
    name: 'MajorityReportsFeedbacksPage',
    component: () => import('./pages/FeedbacksPage').then(m => m.FeedbacksPage),
    mountPoint: rootRouteRef,
  }),
);

export const FeedbackDetailsPage = plugin.provide(
  createRoutableExtension({
    name: 'MajorityReportsFeedbackDetailsPage',
    component: () => import('./pages/FeedbackDetailsPage').then(m => m.FeedbackDetailsPage),
    mountPoint: rootRouteRef,
  }),
);
