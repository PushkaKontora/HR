import {ProfileBlock, ProfileBlockProps} from '../../profile-block';
import {ResumeTitle} from '../../../../styled/resume/resume-title';
import {getFullName} from '../../../../../utils/profile';
import {useState} from 'react';
import {useAppDispatch, useAppSelector} from '../../../../../app/hooks';
import {toast} from 'react-toastify';
import {FORM_NAME, HumanNameForm, HumanNameFormData} from '../../../../human-name-form/human-name-form';
import {setUser} from '../../../../../features/general/general-slice';
import {updateName} from '../../../../../service/async-actions/async-actions-profile';

export function ProfileName() {
  const [showForm, setShowForm] = useState(false);

  const user = useAppSelector((state) => state.general.user);
  const dispatch = useAppDispatch();

  const handleSubmit = (data: HumanNameFormData) => {
    if (user) {
      const arg = {
        id: user.id,
        surname: data.surname,
        name: data.name,
        patronymic: data.patronymic
      };

      dispatch(updateName(arg))
        .then(
          () => {
            //setSaveDisabled(false);
            setShowForm(false);
            toast.success('ФИО успешно изменены');
          }
        );
    }
  };

  const input: ProfileBlockProps = {
    title: 'Имя профиля',
    description: 'Имя будет отображаться в вашем профиле. Также ваше имя сможет увидеть руководитель департамента.',
    buttons: [
      {text: 'Изменить', onClick: () => {setShowForm(true);}, showing: !showForm},
      {text: 'Сохранить', showing: showForm, form: FORM_NAME},
      {text: 'Отмена', onClick: () => {setShowForm(false);}, showing: showForm}
    ]
  };

  return (
    <ProfileBlock
      {...input}>
      <div>
        {
          !showForm &&
            <ResumeTitle>
              {getFullName(user)}
            </ResumeTitle>
        }
        {
          showForm &&
            <div>
              <HumanNameForm submit={handleSubmit}/>
            </div>
        }
      </div>
    </ProfileBlock>
  );
}
