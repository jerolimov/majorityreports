import React from 'react';
import { Link } from 'react-router-dom';

import AppBar_ from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Grid from '@mui/material/Grid';
// import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
// import Badge from '@mui/material/Badge';

// import NotificationsIcon from '@mui/icons-material/Notifications';
// import MoreIcon from '@mui/icons-material/MoreVert';

import { GlobalSearch } from './GlobalSearch';

export const AppBar = () => {
  return (
    <AppBar_ position="sticky" color="inherit">
      <Toolbar>
        <Grid container alignItems="center" sx={{ marginTop: 1, marginBottom: 1 }}>
          <Grid item md={4}>
            {/* <IconButton
              size="large"
              edge="start"
              color="inherit"
              aria-label="open drawer"
              sx={{ mr: 2 }}
            >
              <MenuIcon />
            </IconButton> */}
            <Link to="/">
              <Typography
                component="div"
                variant="h6"
                noWrap
                sx={{ display: { xs: 'none', sm: 'block' }, marginLeft: 1 }}
              >
                ✨ majority reports 🔮
              </Typography>
            </Link>
          </Grid>
          <Grid item md={4}>
            <GlobalSearch />
          </Grid>
          <Grid item md={4} textAlign="right">
            {/* <IconButton
              size="large"
              aria-label="show 17 new notifications"
              color="inherit"
            >
              <Badge badgeContent={17} color="error">
                <NotificationsIcon />
              </Badge>
            </IconButton>
            <IconButton
              size="large"
              aria-label="show more"
              // aria-controls={mobileMenuId}
              aria-haspopup="true"
              // onClick={handleMobileMenuOpen}
              color="inherit"
            >
              <MoreIcon />
            </IconButton> */}
          </Grid>
        </Grid>
      </Toolbar>
    </AppBar_>
  );
};
