import {
  createPlugin,
  createRoutableExtension,
} from '@backstage/core-plugin-api';

import { rootRouteRef } from './routes';

export const majorityreportsCorePlugin = createPlugin({
  id: 'majorityreports-core',
  routes: {
    root: rootRouteRef,
  },
});

export const MajorityreportsCorePage = majorityreportsCorePlugin.provide(
  createRoutableExtension({
    name: 'MajorityreportsCorePage',
    component: () =>
      import('./components/ExampleComponent').then(m => m.ExampleComponent),
    mountPoint: rootRouteRef,
  }),
);
