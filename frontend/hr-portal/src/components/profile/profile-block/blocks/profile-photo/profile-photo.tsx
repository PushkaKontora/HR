import {InputData} from '../../../../forms/types/form-input-props';
import {Image, ImageLabel} from '../../../../../pages/profile-page/styles';
import placeholder from '../../../../../assets/img/profile/placeholder.jpg';
import {ProfileBlock, ProfileBlockProps} from '../../profile-block';
import {useAppDispatch, useAppSelector} from '../../../../../app/hooks';
import {FileLoadInput} from '../../../../file-load-form/file-load-input';
import {IMAGE_FORMATS} from '../../../../../const/approved-file-formats';
import {useRef} from 'react';
import {toast} from 'react-toastify';
import {deleteUserPhoto, loadUserPhoto} from '../../../../../service/async-actions/async-actions-profile';
import {useForm} from 'react-hook-form';

export function ProfilePhoto() {
  const user = useAppSelector((state) => state.general.user);
  const dispatch = useAppDispatch();

  const submit = (file: File) => {
    if (user) {
      const data = new FormData();
      data.append('photo', file);

      dispatch(loadUserPhoto({id: user?.id, data: data}))
        .then(() => {
          toast.success('Новое фото профиля успешно загружено');
        });
    }
  };

  const photoInputRef = useRef<HTMLInputElement | null>(null);
  const FORM_NAME = 'IMAGE_LOAD_FORM';

  const input: ProfileBlockProps = {
    title: 'Фото профиля',
    description: 'Фото профиля появится на странице вашей учётной записи. Ваше фото сможет увидеть руководитель департамента.',
    buttons: [
      {text: 'Удалить',
        onClick: () => {
          if (user) {
            dispatch(deleteUserPhoto({id: user?.id}))
              .then(() => {
                toast.error('Фото профиля удалено');
              });
          }
        }, showing: true},
      {text: 'Загрузить',
        onClick: () => {
          photoInputRef.current?.click();
        }, showing: true}
    ]
  };

  const {
    register
  } = useForm({
    mode: 'onChange'
  });

  return (
    <ProfileBlock
      {...input}>

      <form id={FORM_NAME}>
        <FileLoadInput register={register} formats={IMAGE_FORMATS} onFileChange={submit} inputRef={photoInputRef} name={'file'}/>
      </form>

      <div style={{position: 'relative'}}>
        <Image src={user?.photo || placeholder}/>
        <ImageLabel>Пожалуйста загрузите изображение в формате PNG, JPEG.</ImageLabel>
      </div>
    </ProfileBlock>
  );
}