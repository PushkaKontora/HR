import {InputData} from '../../../../forms/types/form-input-props';
import {ProfileBlock, ProfileBlockProps} from '../../profile-block';
import {FORM_NAME, ResumeForm, ResumeFormData} from '../../../../forms/resume-form/resume-form';
import {useAppDispatch, useAppSelector} from '../../../../../app/hooks';
import {useEffect, useState} from 'react';
import {ResumeReady} from '../../../../resume-ready/resume-ready';
import {
  createResumeAction,
  publishResumeAction, unpublishResumeAction,
  updateResumeAction
} from '../../../../../service/async-actions/async-actions-resume';
import {toast} from 'react-toastify';
import {getAuthUser, getResumeById} from '../../../../../service/async-actions/async-actions-user';

export function ProfileResume() {
  const user = useAppSelector((state) => state.general.user);
  const resume = useAppSelector((state) => state.user.resumeUser);
  const dispatch = useAppDispatch();
  const [showForm, setShowForm] = useState(false);

  const submitForm = (data: ResumeFormData, file: File | null, competencies: string[]) => {
    if (user) {
      const formData = new FormData();
      for (const key in data) {
        if (key !== 'document') {
          formData.append(key, data[key as keyof ResumeFormData].toString());
        }
      }

      if (file) {
        formData.append('document', file);
      }

      if (competencies) {
        for (const c of competencies) {
          formData.append('competencies', c);
        }
      }

      if (user?.resume) {
        dispatch(updateResumeAction({resume_id: user.resume.id, data: formData}))
          .then(() => {dispatch(getResumeById(user.resume.id));})
          .then(() => {
            setShowForm(false);
            toast.success('Резюме изменено');
          });
      } else {
        dispatch(createResumeAction({user_id: user.id, data: formData}))
          .then(() => {
            dispatch(getAuthUser(user.id))
              .then(() => {dispatch(getResumeById(user.resume.id));});
            setShowForm(false);
            toast.success('Резюме создано');
          });
      }
    }
  };

  const input: ProfileBlockProps = {
    title: 'Моё резюме',
    description: 'Резюме может быть только одно. Ваше резюме могут просматривать руководители всех департаментов.',
    buttons: [
      {text: 'Создать резюме', onClick: () => {
        setShowForm(true);
      }, showing: !(user?.resume) && !showForm},
      {text: 'Сохранить черновик', showing: showForm, form: FORM_NAME},
      {text: 'Отмена', onClick: () => {
        setShowForm(false);
      }, showing: showForm},
      {text: 'Опубликовать', onClick: () => {
        if (resume) {
          dispatch(publishResumeAction({resume_id: resume.id}))
            .then(() => {dispatch(getResumeById(resume.id));});
        }
      }, showing: (!showForm && Boolean(user?.resume) && !(resume?.published_at))},
      {text: 'Снять с публкации', onClick: () => {
        if (resume) {
          dispatch(unpublishResumeAction({resume_id: resume.id}))
            .then(() => {dispatch(getResumeById(resume.id));});
        }
      }, showing: (!showForm && Boolean(user?.resume) && Boolean(resume?.published_at))},
      {text: 'Изменить', onClick: () => {
        setShowForm(true);
      }, showing: (!showForm && Boolean(user?.resume))}
    ]
  };

  return (
    <ProfileBlock
      {...input}>
      {
        showForm && <ResumeForm submit={submitForm}></ResumeForm>
      }
      {
        !showForm && user?.resume && <ResumeReady/>
      }
    </ProfileBlock>
  );
}