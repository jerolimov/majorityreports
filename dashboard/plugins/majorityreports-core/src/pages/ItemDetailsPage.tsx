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

  return (
    <Page themeId="item">
      <Header title={item?.meta?.title || item?.meta?.name} type="Item" typeLink="./.." />
      <Content>
        <Grid container>
          <Grid item md={6}>
            <AboutCard object={item} />
          </Grid>
          {/* <Grid item md={6}>
            <CountCard />
          </Grid> */}
          <Grid item md={6}>
            <DescriptionCard object={item} />
          </Grid>
          <Grid item md={6}>
            <LabelsCard object={item} />
          </Grid>
          <Grid item md={6}>
            <AnnotationsCard object={item} />
          </Grid>
        </Grid>
      </Content>
    </Page>
  );
}
