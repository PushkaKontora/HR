import { FormInputProps } from '../types/form-input-props';
import AbstractFormInput from './abstract-form-input';
import {XLargeRegular} from '../../styled/fonts/x-large';

function AuthFormInput(props: FormInputProps) {
  return (
    <AbstractFormInput
      normalBorderColor={'#9C9C9C'}
      padding={'20px'}
      inputMarginBottom={'32px'}
      fontComponent={XLargeRegular}
      {...props}/>
  );
}

export default AuthFormInput;
