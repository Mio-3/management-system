import { Box, Divider, Drawer, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Toolbar } from "@mui/material";
import StoreRoundedIcon from "@mui/icons-material/StoreRounded";
import RamenDiningRoundedIcon from "@mui/icons-material/RamenDiningRounded";
import NewReleasesIcon from '@mui/icons-material/NewReleases';
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';
import { CSSProperties } from "react";
import { usePathname } from "next/navigation";
import Link from "next/link";

interface SideBarProps {
  drawerWidth: number;
  mobileOpen: boolean;
  handleDrawerTransitionEnd: () => void;
  handleDrawerClose: () => void;
}

interface menuItem {
  text: string;
  path: string;
  icon: React.ComponentType;
}

const SideBar = ({ drawerWidth, mobileOpen, handleDrawerTransitionEnd, handleDrawerClose }: SideBarProps) => {
  const pathname = usePathname();
  const MenuItems: menuItem[] = [
    { text: "ホーム", path: "/", icon: StoreRoundedIcon },
    { text: "カレンダー", path: "/shifts", icon: RamenDiningRoundedIcon },
    { text: "シフト提出掲示板", path: "/shifts/confirm", icon: NewReleasesIcon},
    { text: "管理者専用", path: "/manager", icon: AdminPanelSettingsIcon},
  ];

  const activeLinkStyle: CSSProperties = {
    textDecoration: "none",
    color: "inherit",
    display: "block",
  };

  const baseLinkStyle: CSSProperties = {
    backgroundColor: "rgba(0, 0, 0, 0.08)",
  }

  const drawer = (
    <div>
      <Toolbar />
      <Divider />
      <List>
        {MenuItems.map((item, index) => (
          <ListItem key={index} disablePadding>
            <Link href={item.path} passHref>
              <ListItemButton sx={pathname === item.path ? baseLinkStyle : activeLinkStyle}>
                <ListItemIcon>
                  <item.icon />
                </ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItemButton>
            </Link>
          </ListItem>
        ))}
      </List>
    </div>
  );

  return (
    <Box component="nav" sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }} aria-label="mailbox folders">
      {/* スマホ版のサイドバー */}
      <Drawer
        variant="temporary"
        open={mobileOpen}
        onTransitionEnd={handleDrawerTransitionEnd}
        onClose={handleDrawerClose}
        ModalProps={{
          keepMounted: true, 
        }}
        sx={{
          display: { xs: "block", sm: "none" },
          "& .MuiDrawer-paper": { boxSizing: "border-box", width: drawerWidth },
        }}
      >
        {drawer}
      </Drawer>

      {/* PC版のサイドバー */}
      <Drawer
        variant="permanent"
        sx={{
          display: { xs: "none", sm: "block" },
          "& .MuiDrawer-paper": { boxSizing: "border-box", width: drawerWidth },
        }}
        open
      >
        {drawer}
      </Drawer>
    </Box>
  );
};

export default SideBar;