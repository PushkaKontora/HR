import {User} from '../../../../../types/user';
import {ProfileBlock, ProfileBlockProps} from '../../profile-block';
import {useEffect, useState} from 'react';
import {ResumeTitle} from '../../../../styled/resume/resume-title';
import ResumeFormInput from '../../../../forms/form-inputs/resume-form-input';
import {useForm} from 'react-hook-form';
import {EMAIL_OPTIONS} from '../../../../../const/forms/input-options';
import {InputData} from '../../../../forms/types/form-input-props';
import {toast} from 'react-toastify';
import {useAppDispatch, useAppSelector} from '../../../../../app/hooks';
import {updateEmailAction} from '../../../../../service/async-actions/async-actions-profile';

type FormData = {
  email: string
}

export function ProfileEmail() {
  const {
    register,
    handleSubmit,
    formState: {errors}
  } = useForm<FormData>({
    mode: 'onChange'
  });
  const fieldData: InputData = {
    name: 'email',
    label: '',
    type: 'email',
    options: {
      required: 'Вы не ввели e-mail',
      ...EMAIL_OPTIONS
    }
  };

  const [showForm, setShowForm] = useState(false);
  const user = useAppSelector((state) => state.general.user);
  //const [userState, setUserState] = useState(props.user);
  const dispatch = useAppDispatch();

  const FORM_NAME = 'EMAIL_UPDATE_FORM';

  const input: ProfileBlockProps = {
    title: 'Почтовый адрес',
    description: 'Ваш почтовый адрес может увидеть только руководитель департамента.',
    buttons: [
      {text: 'Изменить', onClick: () => {setShowForm(true);}, showing: !showForm},
      {text: 'Сохранить', showing: showForm, form: FORM_NAME},
      {text: 'Отмена', onClick: () => {setShowForm(false);}, showing: showForm}
    ]
  };

  const onSubmit = (data: FormData) => {
    if (user) {
      const arg = {
        id: user.id,
        email: data.email
      };

      dispatch(updateEmailAction(arg))
        .then(
          () => {
            //setSaveDisabled(false);
            setShowForm(false);
            toast.success('Email успешно изменен');
          }
        );
    }
  };

  return (
    <ProfileBlock
      {...input}>
      <div>
        {
          !showForm &&
            <ResumeTitle>
              {user?.email}
            </ResumeTitle>
        }
        {
          showForm &&
            <div>
              <form id={FORM_NAME} onSubmit={handleSubmit(onSubmit)}>
                <ResumeFormInput width={'400px'} inputMarginBottom={'16px'} errors={errors} register={register} {...fieldData} defaultValue={user?.email}/>
              </form>
            </div>
        }
      </div>
    </ProfileBlock>
  );
}