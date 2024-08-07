import React from 'react';
import { useParams } from 'react-router-dom';
import useAsync from 'react-use/lib/useAsync';

import {
  Page,
  Header,
  Content,
  Progress,
  ResponseErrorPanel,
} from '@backstage/core-components';

import Grid from '@material-ui/core/Grid';

import { Event } from '@internal/backstage-plugin-majorityreports-common';

import { AboutCard } from '../components/AboutCard';
import { DescriptionCard } from '../components/DescriptionCard';
import { LabelsCard } from '../components/LabelsCard';
import { AnnotationsCard } from '../components/AnnotationsCard';

export const EventDetailsPage = () => {
  const { namespace_name: namespaceName, event_name: eventName } = useParams();

  const { value: event, loading, error } = useAsync(async (): Promise<Event> => {
    const proxyUrl = 'http://localhost:7007/api/proxy/api/';
    const url = new URL('api/namespaces/' + namespaceName + '/events/' + eventName, proxyUrl);
    return fetch(url.toString()).then((response) => response.json());
  }, []);

  if (loading) {
    return <Progress />;
  } else if (error) {
    return <ResponseErrorPanel error={error} />;
  }

  const title = event?.annotations?.['title'] || eventName;

  return (
    <Page themeId="event">
      <Header title={title} type="Event" typeLink="./.." />
      <Content>
        <Grid container>
          <Grid item md={6}>
            <AboutCard object={event} />
          </Grid>
          {/* <Grid item md={6}>
            <CountCard />
          </Grid> */}
          <Grid item md={6}>
            <DescriptionCard annotations={event?.annotations} />
          </Grid>
          <Grid item md={6}>
            <LabelsCard labels={event?.labels} />
          </Grid>
          <Grid item md={6}>
            <AnnotationsCard annotations={event?.annotations} />
          </Grid>
        </Grid>
      </Content>
    </Page>
  );
}
