import React, { PropsWithChildren } from 'react';
import { useLocation } from 'react-router-dom';

import {
  Sidebar,
  SidebarDivider,
  SidebarGroup,
  SidebarItem,
  SidebarPage,
  SidebarScrollWrapper,
  useSidebarOpenState,
  Link,
} from '@backstage/core-components';

import MenuIcon from '@material-ui/icons/Menu';
import HomeIcon from '@material-ui/icons/Dashboard';

import ActorIcon from '@material-ui/icons/Group';
import ItemIcon from '@material-ui/icons/Description';
import EventIcon from '@material-ui/icons/EventNote';
import FeedbackIcon from '@material-ui/icons/RateReview';

import { NamespaceDropdown } from './NamespaceDropdown';

// import {
//   Settings as SidebarSettings,
//   UserSettingsSignInAvatar,
// } from '@backstage/plugin-user-settings';

const SidebarLogo = () => {
  const { isOpen } = useSidebarOpenState();

  return (
    <Link to="/" underline="none" aria-label="Home">
      {isOpen ? <h1>✨ majority reports 🔮</h1> : <h3>🔮</h3>}
    </Link>
  );
};

export const Root = ({ children }: PropsWithChildren<{}>) => {
  const { pathname } = useLocation();
  const namespace = pathname.startsWith('/namespaces/') ?
    pathname.split('/')[2] :
    null;

  return (
    <SidebarPage>
      <Sidebar>
        <SidebarLogo />
        <SidebarDivider />
        <SidebarGroup label="Menu" icon={<MenuIcon />}>
          <NamespaceDropdown />
          <SidebarDivider />
          <SidebarScrollWrapper>
            {!namespace ? (
              <>
                <SidebarItem icon={HomeIcon} to="/namespaces" text="Dashboard" />
                <SidebarDivider />
                <SidebarItem icon={ActorIcon} to="/actors" text="Actors" />
                <SidebarItem icon={ItemIcon} to="/items" text="Items" />
                <SidebarItem icon={EventIcon} to="/events" text="Events" />
                <SidebarItem icon={FeedbackIcon} to="/feedbacks" text="Feedback" />
              </>
            ) : ( 
              <>
                <SidebarItem icon={HomeIcon} to={`/namespaces/${namespace}/dashboard`} text="Dashboard" />
                <SidebarDivider />
                <SidebarItem icon={ActorIcon} to={`/namespaces/${namespace}/actors`} text="Actors" />
                <SidebarItem icon={ItemIcon} to={`/namespaces/${namespace}/items`} text="Items" />
                <SidebarItem icon={EventIcon} to={`/namespaces/${namespace}/events`} text="Events" />
                <SidebarItem icon={FeedbackIcon} to={`/namespaces/${namespace}/feedbacks`} text="Feedback" />
              </>
            )}
          </SidebarScrollWrapper>
        </SidebarGroup>
        {/* <SidebarSpace />
        <SidebarDivider />
        <SidebarGroup
          label="Settings"
          icon={<UserSettingsSignInAvatar />}
          to="/settings"
        >
          <SidebarSettings />
        </SidebarGroup> */}
      </Sidebar>
      {children}
    </SidebarPage>
  );
};
