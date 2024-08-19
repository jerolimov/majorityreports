import React from 'react';

import Chip from '@material-ui/core/Chip';

import { Namespace, Actor, Event, Feedback, Item } from '@internal/backstage-plugin-majorityreports-common';

export const Tags = ({ object }: { object?: Namespace | Actor | Item | Event | Feedback }) => {
  const tags = object?.meta?.tags;

  return tags?.map((tag) => (
    <Chip key={tag} label={tag} size="small" />
  ));
};
