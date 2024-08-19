import React from 'react';
import { useParams } from 'react-router-dom';

import {
  Page,
  Header,
  Content,
  Progress,
  ResponseErrorPanel,
} from '@backstage/core-components';

import Grid from '@material-ui/core/Grid';

import { useQuery } from '@tanstack/react-query';

import { Event } from '@internal/backstage-plugin-majorityreports-common';

import { AboutCard } from '../components/AboutCard';
import { DescriptionCard } from '../components/DescriptionCard';
import { LabelsCard } from '../components/LabelsCard';
import { AnnotationsCard } from '../components/AnnotationsCard';

export const EventDetailsPage = () => {
  const { namespace_name: namespaceName, event_name: eventName } = useParams();

  const result = useQuery<Event>({
    queryKey: ['events', namespaceName, eventName],
    queryFn: function getNamespaces() {
      const proxyUrl = 'http://localhost:7007/api/proxy/api/';
      const url = new URL('api/namespaces/' + namespaceName + '/events/' + eventName, proxyUrl);
      return fetch(url.toString()).then((response) => response.json());
    },
  });

  if (result.isLoading) {
    return <Progress />;
  } else if (result.error) {
    return <ResponseErrorPanel error={result.error} />;
  }

  const event = result.data;

  return (
    <Page themeId="event">
      <Header title={event?.meta.title || event?.meta.name} type="Event" typeLink="./.." />
      <Content>
        <Grid container>
          <Grid item md={6}>
            <AboutCard object={event} />
          </Grid>
          {/* <Grid item md={6}>
            <CountCard />
          </Grid> */}
          <Grid item md={6}>
            <DescriptionCard object={event} />
          </Grid>
          <Grid item md={6}>
            <LabelsCard object={event} />
          </Grid>
          <Grid item md={6}>
            <AnnotationsCard object={event} />
          </Grid>
        </Grid>
      </Content>
    </Page>
  );
}
