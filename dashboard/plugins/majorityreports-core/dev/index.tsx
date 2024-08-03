import React from 'react';
import { createDevApp } from '@backstage/dev-utils';
import { majorityreportsCorePlugin, MajorityreportsCorePage } from '../src/plugin';

createDevApp()
  .registerPlugin(majorityreportsCorePlugin)
  .addPage({
    element: <MajorityreportsCorePage />,
    title: 'Root Page',
    path: '/majorityreports-core',
  })
  .render();
