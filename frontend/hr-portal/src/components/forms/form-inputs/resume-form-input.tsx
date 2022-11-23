import { FormInputProps } from '../types/form-input-props';
import {XLargeRegular} from '../../styled/fonts/x-large';
import AbstractFormInput from './abstract-form-input';
import {LargeLight} from '../../styled/fonts/large';

type ResumeFormInputProps = {
  width: string,
  inputMarginBottom?: string
} & FormInputProps;

function ResumeFormInput(props: ResumeFormInputProps) {
  return (
    <AbstractFormInput
      normalBorderColor={'#000'}
      padding={'14.5px 16px'}
      borderWidth={'0.5px'}
      fontComponent={LargeLight}
      inputRef={props.inputRef}
      inputMarginBottom={props.inputMarginBottom || '0px'}
      {...props}/>
  );
}

export default ResumeFormInput;
