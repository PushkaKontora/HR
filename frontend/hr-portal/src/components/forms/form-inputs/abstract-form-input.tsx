import { FormInputProps } from '../types/form-input-props';
import styled, {StyledComponent} from 'styled-components';
import {InputField, InputFieldProps} from '../styled/input-field';
import {MutableRefObject, RefObject} from 'react';

const Parent = styled.div<{marginBottom: string}>`
  margin-bottom: ${props => props.marginBottom};
`;

const ErrorField = styled.div`
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  
  margin-top: 0.5rem;
  margin-left: 0.5rem;
  
  color: #C52B1A;
  
  display: block;
`;

const LabelField = styled.label`
  font-size: 16px;
  letter-spacing: 0.05em;
  
  margin-bottom: 8px;
  
  display: block;
`;

type AbstractFormInputProps = {
  normalBorderColor: string,
  padding: string,
  inputMarginBottom: string,
  fontComponent: StyledComponent<'div', any>
  inputRef?: RefObject<typeof InputField>
} & FormInputProps;

function AbstractFormInput(props: AbstractFormInputProps) {
  const fieldName = props.name;

  return (
    <Parent marginBottom={props.inputMarginBottom}>
      <LabelField>{props.label}</LabelField>

      <props.fontComponent>
        <InputField
          normalBorderColor={props.normalBorderColor}
          padding={props.padding}
          type={props.type}
          placeholder={props.placeholder}
          ref={props.inputRef}
          {...props.register(props.name, props.options)}
          aria-invalid={props.errors[fieldName] ? 'true' : 'false'}/>
      </props.fontComponent>

      <ErrorField>
        {[props.errors[fieldName]] && [props.errors[fieldName]?.message]}
      </ErrorField>
    </Parent>
  );
}

export default AbstractFormInput;
