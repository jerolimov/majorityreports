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

export const ActorsPage = plugin.provide(
  createRoutableExtension({
    name: 'MajorityReportsActorsPage',
    component: () => import('./pages/ActorsPage').then(m => m.ActorsPage),
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

export const EventsPage = plugin.provide(
  createRoutableExtension({
    name: 'MajorityReportsEventsPage',
    component: () => import('./pages/EventsPage').then(m => m.EventsPage),
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
