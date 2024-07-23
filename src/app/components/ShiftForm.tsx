import { Box, Button, ButtonGroup, IconButton, ListItemIcon, MenuItem, Stack, TextField, Typography } from "@mui/material";
import React from "react";
import CloseIcon from "@mui/icons-material/Close";
import { Controller, useForm } from "react-hook-form";
import WbSunnyIcon from "@mui/icons-material/WbSunny";
import NightlightIcon from "@mui/icons-material/Nightlight";
import MoreTimeIcon from "@mui/icons-material/MoreTime";

interface ShiftFormProps {
  onSaveShift: (data: ShiftFormValues) => void;
  onCloseForm: () => void;
  isEntryDrawerOpen: boolean;
}

export interface ShiftFormValues {
  date: string;
  category: string;
}

const ShiftForm = ({ onSaveShift, onCloseForm, isEntryDrawerOpen }: ShiftFormProps) => {
  const formWidth = 320;
  const { handleSubmit, control } = useForm<ShiftFormValues>();

  const onSubmit = async (data: ShiftFormValues) => {
    onSaveShift(data);
    onCloseForm();
  };

  return (
    <Box
      sx={{
        position: "fixed",
        top: 64,
        right: isEntryDrawerOpen ? -4 : -327, // フォームの位置を調整
        width: formWidth,
        height: "100%",
        bgcolor: "background.paper",
        zIndex: (theme) => theme.zIndex.drawer - 1,
        transition: (theme) =>
          theme.transitions.create("right", {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
          }),
        p: 2, // 内部の余白
        boxSizing: "border-box", // ボーダーとパディングをwidthに含める
        boxShadow: "0px 0px 15px -5px #777777",
      }}
    >
      {/* 入力エリアヘッダー */}
      <Box display={"flex"} justifyContent={"space-between"} mb={2}>
        <Typography variant="h6">シフト希望入力</Typography>
        {/* 閉じるボタン */}
        <IconButton
          onClick={onCloseForm}
          sx={{
            color: (theme) => theme.palette.grey[500],
          }}
        >
          <CloseIcon />
        </IconButton>
      </Box>
      {/* フォーム要素 */}
      <Box component={"form"} onSubmit={handleSubmit(onSubmit)}>
        <Stack spacing={2}>
          {/* 日付 */}
          <Controller
            name="date"
            control={control}
            defaultValue=""
            render={({ field }) => (
              <TextField
                {...field}
                label="日付"
                type="date"
                InputLabelProps={{
                  shrink: true,
                }}
              />
            )}
          />

          {/* カテゴリ */}
          <Controller
            name="category"
            control={control}
            defaultValue=""
            render={({ field }) => (
              <TextField {...field} id="カテゴリ" label="カテゴリ" select>
                <MenuItem value="">
                  <em>空欄</em>
                </MenuItem>
                <MenuItem value="noon">
                  <ListItemIcon>
                    <WbSunnyIcon />
                  </ListItemIcon>
                  昼
                </MenuItem>
                <MenuItem value="night">
                  <ListItemIcon>
                    <NightlightIcon />
                  </ListItemIcon>
                  夜
                </MenuItem>
                <MenuItem value="all-day">
                  <ListItemIcon>
                    <MoreTimeIcon />
                  </ListItemIcon>
                  1日
                </MenuItem>
                <MenuItem value="cross">
                  <ListItemIcon>
                    <CloseIcon />
                  </ListItemIcon>
                  出勤不可
                </MenuItem>
              </TextField>
            )}
          />
          {/* 保存ボタン */}
          <Button type="submit" variant="contained" color={"primary"} fullWidth>
            保存
          </Button>
        </Stack>
      </Box>
    </Box>
  );
};
export default ShiftForm;
