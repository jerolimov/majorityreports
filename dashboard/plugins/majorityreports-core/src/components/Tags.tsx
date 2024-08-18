import React from 'react';

import Chip from '@material-ui/core/Chip';

import { Namespace /*, Actor, Event, Feedback, Item*/ } from '@internal/backstage-plugin-majorityreports-common';

export const Tags = ({ object }: { object?: Namespace /*| Actor | Item | Event | Feedback*/ }) => {
  // TODO: remove tags support
  const tags = object?.meta?.tags || object?.meta?.labels?.['tags']?.split(',').map((tag) => tag.trim()).filter(Boolean);

  return tags?.map((tag) => (
    <Chip key={tag} label={tag} size="small" />
  ));
};
