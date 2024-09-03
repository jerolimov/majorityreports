import React from 'react';

import Button from '@mui/material/Button';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';

import ArrowDownIcon from '@material-ui/icons/KeyboardArrowDown';

import { useQuery } from '@tanstack/react-query';

import { useNamespace } from '../../hooks/useNamespace';

import { NamespaceList } from '@internal/backstage-plugin-majorityreports-common';

export const NamespaceDropdown = () => {
  const [namespace, setNamespace] = useNamespace();

  const result = useQuery<NamespaceList>({
    queryKey: ['namespaces', 0, 100],
    queryFn: function getNamespaces() {
      const proxyUrl = 'http://localhost:7007/api/proxy/api/';
      const url = new URL('api/namespaces', proxyUrl);
      url.searchParams.set('limit', '100');    
      return fetch(url.toString()).then((response) => response.json());
    },
  });

  const namespaces = result.data?.items;

  // From MUI doc
  const [anchorEl, setAnchorEl] = React.useState<HTMLElement | null>(null);
  const open = Boolean(anchorEl);

  const handleOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleSelectAllNamespacen = () => {
    setNamespace(null);
    handleClose();
  };

  const handleSelectNamespace = (event: React.MouseEvent<HTMLElement>) => {
    const newNamespace = event.currentTarget.getAttribute('data-namespace');
    setNamespace(newNamespace);
    handleClose();
  };

  return (
    <>
      <Button
        id="namespace-button"
        aria-controls={open ? 'namespace-menu' : undefined}
        aria-haspopup="true"
        aria-expanded={open ? 'true' : undefined}
        variant="outlined"
        color="inherit"
        disableRipple
        disableElevation
        onClick={handleOpen}
        endIcon={<ArrowDownIcon />}
        sx={{ alignSelf: 'stretch', margin: 2, textTransform: 'none', textAlign: 'left' }}
      >
        {namespace || 'All namespaces'}
      </Button>
      <Menu
        id="namespace-menu"
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        MenuListProps={{
          'aria-labelledby': 'namespace-button',
        }}
      >
        <MenuItem
          href="/namespaces"
          onClick={handleSelectAllNamespacen}
          selected={!namespace}
          disableRipple
          divider
          children="All namespaces"
        />
        {namespaces?.map(({ meta: { name }}) => (
          <MenuItem
            key={name}
            href={`/namespaces/${name}`}
            onClick={handleSelectNamespace}
            disableRipple
            selected={name === namespace}
            data-namespace={name}
            children={name}
          />
        ))}
      </Menu>
    </>
  );
}
