import {useForm, Controller} from 'react-hook-form';
import {XLargeRegular} from '../../styled/fonts/x-large';
import {ResumeFieldContainer, ResumeFieldLabel} from '../../styled/resume/styles';
import ResumeFormInput from '../form-inputs/resume-form-input';
import {InputData} from '../types/form-input-props';
import {FileLoadInput} from '../../file-load-form/file-load-input';
import {FileLoadComponent} from '../../../file-load-component/file-load-component';
import {RESUME_FORMATS} from '../../../const/approved-file-formats';
import {ProfileSelect} from '../../selects/profile-select/profile-select';
import {ExperienceSelect, OPTIONS} from '../../selects/experience-select/experience-select';
import {CompetenciesSelect} from '../../selects/competencies-select/competencies-select';
import {useAppDispatch, useAppSelector} from '../../../app/hooks';
import {createResumeAction, updateResumeAction} from '../../../service/async-actions/async-actions-resume';
import {CompetencyList} from '../../../competency-list/competency-list';
import {ResumeUser} from '../../../types/resume';
import {extractFileNameFromYandex} from '../../../utils/resume';
import {useState} from 'react';

export type ResumeFormData = {
  desired_job: string,
  document: File,
  experience: string,
  desired_salary: number,
  competencies: string[]
}

export const DOC_FIELD_NAME = 'document';
export const FORM_NAME = 'PROFILE_RESUME_FORM';

export type ResumeFormProps = {
  submit: (data: ResumeFormData, file: File | null, competencies: string[]) => void
}

export function ResumeForm({submit}: ResumeFormProps) {
  const {
    register,
    handleSubmit,
    control,
    formState: {errors}
  } = useForm<ResumeFormData>({
    mode: 'onChange'
  });

  const resume = useAppSelector((state) => state.user.resumeUser);
  const [bufferComps, setBufferComps] = useState(resume?.competencies ? resume.competencies.slice() : []);
  const [newResume, setNewResume] = useState<File | null>(null);

  const onCompetencyChange = (e: any) => {
    setBufferComps(bufferComps.concat(e.value));
  };

  const submitForm = (data: ResumeFormData) => {
    submit(data, newResume, bufferComps);
  };

  const inputs: InputData[] = [
    {
      name: 'desired_job',
      label: '',
      type: 'text',
      options: {
        required: 'Введите желаемую компетенцию'
      },
      defaultValue: resume?.desired_job
    },
    {
      name: 'desired_salary',
      label: '',
      type: 'number',
      options: {
        valueAsNumber: true,
        value: resume?.desired_salary,
        min: 0
      },
      defaultValue: '10000'
    }
  ];

  return (
    <form id={FORM_NAME} onSubmit={handleSubmit(submitForm)}>
      <ResumeFieldContainer>
        <ResumeFieldLabel>Желаемая должность</ResumeFieldLabel>
        <ResumeFormInput width={'440px'} errors={errors} register={register} {...inputs[0]}/>
      </ResumeFieldContainer>
      <ResumeFieldContainer>
        <ResumeFieldLabel>Резюме в формате PDF</ResumeFieldLabel>
        <FileLoadComponent
          onUpdate={(file: File) => {
            setNewResume(file);
          }}
          register={register}
          fieldName={DOC_FIELD_NAME}
          initFileName={extractFileNameFromYandex(resume?.document)}/>
      </ResumeFieldContainer>
      <ResumeFieldContainer>
        <ResumeFieldLabel>Опыт работы</ResumeFieldLabel>
        <Controller
          control={control}
          defaultValue={resume?.experience || 'no_experience'}
          render={({field: {onChange, value}}) => <ExperienceSelect onChange={(val) => onChange(val.value)} controllerValue={value} name={'experience'} selectedValue={resume?.experience}/>}
          name={'experience'}/>
      </ResumeFieldContainer>
      <ResumeFieldContainer>
        <ResumeFieldLabel>Ожидаемая зарплата</ResumeFieldLabel>
        <ResumeFormInput width={'190px'} errors={errors} register={register} {...inputs[1]}/>
      </ResumeFieldContainer>
      <ResumeFieldContainer>
        <ResumeFieldLabel>Мои компетенции</ResumeFieldLabel>
        <CompetencyList values={bufferComps}/>
        <CompetenciesSelect name={'competencies_select'} onChange={onCompetencyChange} selectedComps={bufferComps}/>
      </ResumeFieldContainer>
    </form>
  );
}