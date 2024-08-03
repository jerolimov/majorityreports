import React, { PropsWithChildren } from 'react';

import MenuIcon from '@material-ui/icons/Menu';
import NamespaceIcon from '@material-ui/icons/AccountTree';
import ActorIcon from '@material-ui/icons/Group';
import ItemIcon from '@material-ui/icons/Description';
import EventIcon from '@material-ui/icons/EventNote';
import FeedbackIcon from '@material-ui/icons/RateReview';

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

export const Root = ({ children }: PropsWithChildren<{}>) => (
  <SidebarPage>
    <Sidebar>
      <SidebarLogo />
      <SidebarDivider />
      <SidebarGroup label="Menu" icon={<MenuIcon />}>
        {/* <SidebarItem icon={HomeIcon} to="/" text="Home" /> */}
        {/* <SidebarDivider /> */}
        <SidebarScrollWrapper>
          <SidebarItem icon={NamespaceIcon} to="/namespaces" text="Namespaces" />
          <SidebarItem icon={ActorIcon} to="/actors" text="Actors" />
          <SidebarItem icon={ItemIcon} to="/items" text="Items" />
          <SidebarItem icon={EventIcon} to="/events" text="Events" />
          <SidebarItem icon={FeedbackIcon} to="/feedbacks" text="Feedback" />
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
