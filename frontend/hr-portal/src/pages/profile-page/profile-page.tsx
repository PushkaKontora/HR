import {ProfileHeader} from '../../components/profile/profile-header/profile-header';
import {Content} from '../../components/styled/markup/content';
import {ProfileBlock, ProfileBlockProps} from '../../components/profile/profile-block/profile-block';
import {ResumeTitle} from '../../components/styled/resume/resume-title';
import {BlueButton} from '../../components/styled/buttons/blue-button';
import {createRef, Fragment, ReactNode, useRef, useState} from 'react';
import Modal from '../../reused-components/modal/modal';
import {LargeRegular} from '../../components/styled/fonts/large';
import {GrayButton} from '../../components/styled/buttons/gray-button';
import {ModalButtonContainer, Image, ImageLabel} from './styles';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {getDate, getFullName} from '../../utils/profile';
import placeholder from '../../assets/img/profile/placeholder.jpg';
import {ResetPasswordForm} from '../../components/profile/reset-password-form/reset-password-form';
import {ProfileDelete} from '../../components/profile/profile-block/blocks/profile-delete/profile-delete';
import {ProfilePassword} from '../../components/profile/profile-block/blocks/profile-password/profile-password';
import {ProfileEmail} from '../../components/profile/profile-block/blocks/profile-email/profile-email';
import {ProfileName} from '../../components/profile/profile-block/blocks/profile-name/profile-name';
import {ProfilePhoto} from '../../components/profile/profile-block/blocks/profile-photo/profile-photo';
import {ProfileResume} from '../../components/profile/profile-block/blocks/profile-resume/profile-resume';
import {deleteUser} from '../../service/async-actions/async-actions-delete-user';
import {dropToken} from '../../service/token-manager';

function ProfilePage() {
  const [showingModal, setShowingModal] = useState(false);
  const toScrollRef = useRef<HTMLDivElement | null>(null);

  const user = useAppSelector((state) => state.general.user);
  const dispatch = useAppDispatch();

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
          <GrayButton
            as={'button'}
            style={{flex: 1, marginRight: '20px'}}
            onClick={() => {setShowingModal(false);}}>
            Отмена
          </GrayButton>
          <BlueButton
            as={'button'}
            style={{flex: 1}}
            onClick={() => {
              if (user) {
                dispatch(deleteUser({id: user.id}))
                  .then(() => {
                    dropToken();
                    window.location.reload();
                  });
              }
            }}>
            Удалить мой аккаунт
          </BlueButton>
        </ModalButtonContainer>
      </Modal>

      <ProfileHeader onSettingsClick={onSettingsClick} user={user}/>
      <Content style={{marginTop: '80px'}}>
        <ProfileResume/>

        <div ref={toScrollRef}></div>
        <ProfilePhoto/>

        <ProfileName/>
        <ProfileEmail/>
        <ProfilePassword/>
        <ProfileDelete onDelete={() => {setShowingModal(true);}}/>
      </Content>
    </>
  );
}

export default ProfilePage;
