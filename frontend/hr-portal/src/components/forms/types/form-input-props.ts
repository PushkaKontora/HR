type InputData = {
  options: any,
  label: string,
  name: string,
  type: string
}

type FormInputProps = {
  errors: any,
  register: any
} & InputData;

export type {InputData, FormInputProps};
