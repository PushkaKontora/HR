import {InputFieldProps} from '../styled/input-field';

type InputData = {
  options: any,
  label: string,
  name: string,
  type: string
}

type FormInputProps = {
  errors: any,
  register: any
} & InputData & InputFieldProps;

export type {InputData, FormInputProps};
