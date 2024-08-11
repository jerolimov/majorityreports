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

import { Item } from '@internal/backstage-plugin-majorityreports-common';

import { AboutCard } from '../components/AboutCard';
import { DescriptionCard } from '../components/DescriptionCard';
import { LabelsCard } from '../components/LabelsCard';
import { AnnotationsCard } from '../components/AnnotationsCard';

export const ItemDetailsPage = () => {
  const { namespace_name: namespaceName, item_name: itemName } = useParams();

  const result = useQuery<Item>({
    queryKey: ['items', namespaceName, itemName],
    queryFn: function getNamespaces() {
      const proxyUrl = 'http://localhost:7007/api/proxy/api/';
      const url = new URL('api/namespaces/' + namespaceName + '/items/' + itemName, proxyUrl);
      return fetch(url.toString()).then((response) => response.json());
    },
  });

  if (result.isLoading) {
    return <Progress />;
  } else if (result.error) {
    return <ResponseErrorPanel error={result.error} />;
  }

  const item = result.data;
  const title = item?.annotations?.['title'] || itemName;

  return (
    <Page themeId="item">
      <Header title={title} type="Item" typeLink="./.." />
      <Content>
        <Grid container>
          <Grid item md={6}>
            <AboutCard object={item} />
          </Grid>
          {/* <Grid item md={6}>
            <CountCard />
          </Grid> */}
          <Grid item md={6}>
            <DescriptionCard annotations={item?.annotations} />
          </Grid>
          <Grid item md={6}>
            <LabelsCard labels={item?.labels} />
          </Grid>
          <Grid item md={6}>
            <AnnotationsCard annotations={item?.annotations} />
          </Grid>
        </Grid>
      </Content>
    </Page>
  );
}
