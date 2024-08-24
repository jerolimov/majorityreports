import React from 'react';
import { useParams } from 'react-router-dom';

import {
  Page,
  Header,
  Content,
  ResponseErrorPanel,
} from '@backstage/core-components';

import Grid from '@material-ui/core/Grid';

import { useQuery } from '@tanstack/react-query';

import { Item } from '@internal/backstage-plugin-majorityreports-common';

import { AboutCard } from '../components/AboutCard';
import { DescriptionCard } from '../components/DescriptionCard';
import { LabelsCard } from '../components/LabelsCard';
import { AnnotationsCard } from '../components/AnnotationsCard';
import { FeaturesCard } from '../components/FeaturesCard';

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

  if (result.error) {
    return <ResponseErrorPanel error={result.error} />;
  }

  const item = result.data;

  return (
    <Page themeId="item">
      <Header title={item?.meta?.title || item?.meta?.name} type="Item" typeLink="./.." />
      <Content>
        <Grid container>
          <Grid item container md={6}>
            <Grid item sm={12}>
              <AboutCard object={item} />
            </Grid>
            <Grid item sm={12}>
              <LabelsCard object={item} />
              </Grid>
              <Grid item sm={12}>
              <AnnotationsCard object={item} />
            </Grid>
            <Grid item sm={12}>
              <FeaturesCard object={item} />
            </Grid>
          </Grid>
          <Grid item md={6}>
            {/* <Grid item md={6}>
              <CountCard />
            </Grid> */}
            <DescriptionCard object={item} />
          </Grid>
        </Grid>
      </Content>
    </Page>
  );
}
