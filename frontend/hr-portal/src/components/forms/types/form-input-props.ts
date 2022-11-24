import {MutableRefObject, RefObject} from 'react';
import {InputField} from '../styled/input-field';

type InputData = {
  options: any,
  label: string,
  name: string,
  type?: string,
  placeholder?: string,
  defaultValue?: string
}

type FormInputProps = {
  errors: any,
  register: any
  inputRef?: RefObject<typeof InputField>
} & InputData;

export type {InputData, FormInputProps};
