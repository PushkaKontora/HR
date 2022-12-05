import {InputData} from '../../../../forms/types/form-input-props';
import {ProfileBlock, ProfileBlockProps} from '../../profile-block';
import {FORM_NAME, ResumeForm, ResumeFormData} from '../../../../forms/resume-form/resume-form';
import {useAppDispatch, useAppSelector} from '../../../../../app/hooks';
import {useEffect, useState} from 'react';
import {ResumeReady} from '../../../../resume-ready/resume-ready';
import {
  createResumeAction, deleteDocument,
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

  const checkForEmptyForm = (data: ResumeFormData, file: File | null | undefined, competencies: string[]) => {
    return !data?.experience
      && !data?.desired_job
      && !data?.desired_salary
      && !file
      && !competencies?.length;
  };

  const submitForm = (data: ResumeFormData, file: File | null | undefined, competencies: string[]) => {
    if (user) {
      if (checkForEmptyForm(data, file, competencies)) {
        setShowForm(false);
        return;
      }

      const formData = new FormData();
      formData.append('desired_job', data?.desired_job || '');
      if (data.experience) {
        formData.append('experience', data.experience);
      }

      formData.append('desired_salary', data?.desired_salary ? data.desired_salary.toString() : '0');

      if (file) {
        formData.append('document', file);
      } else if (file === null) {
        if (resume) {
          dispatch(deleteDocument(resume?.id));
        }
      }

      if (competencies.length > 0) {
        for (const c of competencies) {
          formData.append('competencies', c);
        }
      } else {
        formData.append('competencies', '');
      }

      if (user?.resume) {
        dispatch(updateResumeAction({resume_id: user.resume.id, data: formData}))
          .then(() => {dispatch(getResumeById(user.resume.id));})
          .then(() => {
            setShowForm(false);
            toast.success('Черновик сохранен');
          });
      } else {
        dispatch(createResumeAction({user_id: user.id, data: formData}))
          .then(() => {
            dispatch(getAuthUser(user.id))
              .then(() => {dispatch(getResumeById(user.resume.id));});
            setShowForm(false);
            toast.success('Черновик сохранен');
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
          if (resume.desired_job && resume.document) {
            dispatch(publishResumeAction({resume_id: resume.id}))
              .then(() => {
                dispatch(getResumeById(resume.id));
                toast.success('Резюме опубликовано');
              });
          } else {
            toast.error('Чтобы опубликовать резюме, укажите как минимум желаемую должность и прикрепите файл PDF');
          }
        }
      }, showing: (!showForm && Boolean(user?.resume) && !(resume?.published_at))},
      {text: 'Снять с публкации', onClick: () => {
        if (resume) {
          dispatch(unpublishResumeAction({resume_id: resume.id}))
            .then(() => {
              dispatch(getResumeById(resume.id));
              toast.error('Резюме снято с публикации');
            });
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