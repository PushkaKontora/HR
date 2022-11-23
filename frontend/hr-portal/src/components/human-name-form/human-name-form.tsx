import { useRef } from 'react';
import {useForm} from 'react-hook-form';
import {InputData} from '../forms/types/form-input-props';
import {PASSWORD_OPTIONS} from '../../const/forms/input-options';
import ResumeFormInput from '../forms/form-inputs/resume-form-input';
import {InputField} from '../forms/styled/input-field';
import {useAppSelector} from '../../app/hooks';
import {FieldContainer} from './styled/field-container';
import {FieldParent} from './styled/field-parent';

export type HumanNameFormData = {
  name: string,
  surname: string,
  patronymic: string
}

type ResetPasswordFormProps = {
  submit: (data: HumanNameFormData) => void
};

export const FORM_NAME = 'NAME_UPDATE_FORM';

export function HumanNameForm({submit}: ResetPasswordFormProps) {
  const {
    register,
    handleSubmit,
    formState: {errors}
  } = useForm<HumanNameFormData>({
    mode: 'onChange'
  });

  const user = useAppSelector((state) => state.general.user);
  const newPassRef = useRef<typeof InputField>(null);

  const inputs: InputData[] = [
    {
      name: 'surname',
      label: '',
      type: 'text',
      options: {
        required: 'Введите фамилию'
      },
      placeholder: 'Фамилия',
      defaultValue: user?.surname
    },
    {
      name: 'name',
      label: '',
      type: 'text',
      options: {
        required: 'Введите имя',
      },
      placeholder: 'Имя',
      defaultValue: user?.name
    },
    {
      name: 'patronymic',
      label: '',
      type: 'text',
      options: {},
      placeholder: 'Отчество',
      defaultValue: user?.patronymic
    }
  ];

  return (
    <form id={FORM_NAME} onSubmit={handleSubmit(submit)}>
      <FieldParent>
        {
          inputs.map((item, idx) => {
            const ref = item.name === 'new_pass' ? newPassRef : undefined;
            return (
              <FieldContainer key={idx}>
                <ResumeFormInput width={'284px'} inputMarginBottom={'16px'} defaultValue={item.defaultValue} inputRef={ref} errors={errors} register={register} {...item}/>
              </FieldContainer>
            );
          })
        }
      </FieldParent>
    </form>
  );
}
