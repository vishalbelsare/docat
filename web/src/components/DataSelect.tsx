import { FormGroup, MenuItem, TextField } from '@mui/material'
import React, { useState } from 'react'

interface Props {
  emptyMessage: string
  errorMsg?: string
  value?: string
  label: string
  values: string[]
  onChange: (value: string) => void
}

export default function DataSelect(props: Props): JSX.Element {
  const [selectedValue, setSelectedValue] = useState<string>(
    props.value ?? 'none'
  )

  // clear field if selected value is not in options
  if (selectedValue !== 'none' && !props.values.includes(selectedValue)) {
    setSelectedValue('none')
  }

  return (
    <FormGroup>
      <TextField
        onChange={(e: { target: { value: string } }) => {
          setSelectedValue(e.target.value)
          props.onChange(e.target.value)
        }}
        value={props.values.length > 0 ? selectedValue : 'none'}
        label={props.label}
        error={props.errorMsg !== undefined && props.errorMsg !== ''}
        helperText={props.errorMsg}
        select
      >
        <MenuItem value="none" disabled>
          {props.emptyMessage}
        </MenuItem>

        {props.values.map((value) => {
          return (
            <MenuItem key={value} value={value}>
              {value}
            </MenuItem>
          )
        })}
      </TextField>
    </FormGroup>
  )
}
