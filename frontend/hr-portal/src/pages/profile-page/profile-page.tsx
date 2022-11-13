import {ProfileHeader} from '../../components/profile/profile-header/profile-header';
import {Content} from '../../components/styled/markup/content';
import {ProfileBlock, ProfileBlockProps} from '../../components/profile/profile-block/profile-block';
import {ResumeTitle} from '../../components/styled/values/resume-title';
import {BlueButton} from '../../components/styled/buttons/blue-button';
import {createRef, Fragment, ReactNode, useRef, useState} from 'react';
import Modal from '../../reused-components/modal/modal';
import {LargeRegular} from '../../components/styled/fonts/large';
import {GrayButton} from '../../components/styled/buttons/gray-button';
import {ModalButtonContainer, Image, ImageLabel} from './styles';
import {useAppSelector} from '../../app/hooks';
import {getDate, getFullName} from '../../utils/profile';
import placeholder from '../../assets/img/profile/placeholder.jpg';
import {ResetPasswordForm} from '../../components/profile/reset-password-form/reset-password-form';
import {ProfileDelete} from '../../components/profile/profile-block/blocks/profile-delete/profile-delete';
import {ProfilePassword} from '../../components/profile/profile-block/blocks/profile-password/profile-password';

function ProfilePage() {
  const [showingModal, setShowingModal] = useState(false);
  const toScrollRef = useRef<HTMLDivElement | null>(null);

  const user = useAppSelector((state) => state.general.user);


  const refs = {
    resume: {
      empty: useRef(null),
      form: useRef(null),
      view: useRef(null)
    },
    name: {
      form: useRef(null),
      view: useRef(null)
    },
    email: {
      form: useRef(null),
      view: useRef(null)
    },
    password: {
      form: useRef(null),
      view: useRef(null)
    }
  };

  const inputs: ProfileBlockProps[] = [
    {
      title: 'Моё резюме',
      description: 'Резюме может быть только одно. Ваше резюме могут просматривать руководители всех департаментов.',
      buttons: [
        {text: 'Создать резюме', onClick: () => {return;}},
        {text: 'Сохранить черновик', onClick: () => {return;}},
        {text: 'Отмена', onClick: () => {return;}}
      ]
    },
    {
      title: 'Фото профиля',
      description: 'Фото профиля появится на странице вашей учётной записи. Ваше фото сможет увидеть руководитель департамента.',
      buttons: [
        {text: 'Удалить', onClick: () => {return;}},
        {text: 'Загрузить', onClick: () => {return;}}
      ],
      children: (
        <div style={{position: 'relative'}}>
          <Image src={user?.photo || placeholder}/>
          <ImageLabel>Пожалуйста загрузите изображение в формате PNG, JPEG.</ImageLabel>
        </div>
      )
    },
    {
      title: 'Имя профиля',
      description: 'Имя будет отображаться в вашем профиле. Также ваше имя сможет увидеть руководитель департамента.',
      buttons: [
        {text: 'Изменить', onClick: () => {return;}}
      ],
      children: (
        <div><ResumeTitle>{getFullName(user)}</ResumeTitle></div>
      )
    },
    {
      title: 'Почтовый адрес',
      description: 'Ваш почтовый адрес может увидеть только руководитель департамента.',
      buttons: [
        {text: 'Изменить', onClick: () => {return;}}
      ],
      children: (
        <div><ResumeTitle>{user?.email}</ResumeTitle></div>
      )
    }
  ];

  const onSettingsClick = () => {
    if (toScrollRef.current) {
      toScrollRef.current.scrollIntoView({behavior: 'smooth'});
    }
  };

  return (
    <>
      <Modal active={showingModal} setActive={setShowingModal}
        width={885} padding={'60px'}>
        <h4 style={{marginBottom: '16px'}}>Вы действительно уверены, что хотите удалить аккаунт?</h4>
        <LargeRegular style={{marginBottom: '40px'}}>Вся информация, связанная с аккаунтом будет удалена.</LargeRegular>
        <ModalButtonContainer>
          <BlueButton
            as={'button'}
            style={{flex: 1, marginRight: '20px'}}
            onClick={() => {setShowingModal(false);}}>
            Отмена
          </BlueButton>
          <GrayButton as={'button'} style={{flex: 1}}>
            Удалить мой аккаунт
          </GrayButton>
        </ModalButtonContainer>
      </Modal>

      <ProfileHeader onSettingsClick={onSettingsClick} user={user}/>
      <Content style={{marginTop: '80px'}}>
        <div ref={toScrollRef}></div>
        {inputs.map((item ,idx) =>
          <ProfileBlock
            key={idx}
            title={item.title}
            description={item.description}
            buttons={item?.buttons}>
            {item.children}
          </ProfileBlock>)}

        <ProfilePassword user={user}/>
        <ProfileDelete onDelete={() => {setShowingModal(true);}}/>
      </Content>
    </>
  );
}

export default ProfilePage;
