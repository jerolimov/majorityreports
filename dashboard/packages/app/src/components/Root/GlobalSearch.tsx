import React from 'react';

import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';

import SearchIcon from '@mui/icons-material/Search';

// import { Command } from 'cmdk'

export const GlobalSearch = () => {
  const [inputValue, setInputValue] = React.useState('')

  // const [open, setOpen] = React.useState(false)

  // // Toggle the menu when ⌘K is pressed
  // React.useEffect(() => {
  //   const down = (e: any) => {
  //     if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
  //       e.preventDefault()
  //       setOpen((open) => !open)
  //     }
  //   }

  //   document.addEventListener('keydown', down)
  //   return () => document.removeEventListener('keydown', down)
  // }, []);

  return (
    <>
      {/* input value: {inputValue} */}
      <TextField
        fullWidth
        variant="outlined"
        value={inputValue}
        onChange={(event) => setInputValue(event.target.value)}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <SearchIcon />
            </InputAdornment>
          ),
          endAdornment: (
            <InputAdornment position="end" variant="outlined">
              ctrl+k
            </InputAdornment>
          ),
        }}
      />
      {/* <Command label="Command Menu" value={inputValue}>
        <Command.Input />
        <Command.List>
          <Command.Empty>No results found.</Command.Empty>

          <Command.Group heading="Letters">
            <Command.Item>a</Command.Item>
            <Command.Item>b</Command.Item>
            <Command.Separator />
            <Command.Item>c</Command.Item>
          </Command.Group>

          <Command.Item>Apple</Command.Item>
        </Command.List>
      </Command> */}
    </>
  );
}
