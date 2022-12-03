import Modal from '../../reused-components/modal/modal';
import React, {ChangeEvent, useEffect, useState} from 'react';
import {DepartmentsShortVersions, setIsEditorVacancyFlag, setIsOpenEditVacancyModal, setIsStartRequestChangeVacancy, setSalaryMax, setSalaryMin, setStateEditVacancy} from '../../features/vacancy/vacancy-slice';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import './modal-edit-vacancy.scss';
import '../../styles/btn-blue-disabled.scss';
import cl from 'classnames';
import Select, {SingleValue} from 'react-select';
import {ExpectedExperience, ExpectedExperienceNameString, expectedExperienceShortVersion, TypeRequestVacancyModal} from '../../const';
import EmployerCreatingNewVacancy from '../employer-creating-new-vacancy/employer-creating-new-vacancy';
import {BlueButton} from '../styled/buttons/blue-button';
import {GrayButton} from '../styled/buttons/gray-button';
import {VacancyPutChangeParams} from '../../types/vacancy-put-change-params';
import {getVacanciesForEmployer, putVacancyChanges} from '../../service/async-actions/async-actions-vacancy';
import ModalBtnStatusVacancy from '../modal-btn-status-vacancy/modal-btn-status-vacancy';

function ModalEditVacancy() {
  const typeRequestModalVacancy = useAppSelector((state) => state.vacancy.typeRequestModalVacancy);
  const vacancyByID = useAppSelector((state) => state.vacancy.vacancyByID);
  const isPublishedVacancy = useAppSelector((state) => state.vacancy.isPublishedVacancy);
  const isOpenEditVacancyModalState = useAppSelector((state) => state.vacancy.isOpenEditVacancyModal);
  const isEditorVacancyText = useAppSelector((state) => state.vacancy.editorTextVacancy);
  const isEditorVacancyFlag = useAppSelector((state) => state.vacancy.isEditorVacancyFlag);
  const isStartRequestChangeVacancy = useAppSelector((state) => state.vacancy.isStartRequestChangeVacancy);
  const [isOpenEditVacancy, setIsOpenEditVacancy] = useState(isOpenEditVacancyModalState);
  const [isPublishStatus, setIsPublishStatus] = useState(isPublishedVacancy);
  const [nameVacancy, setNameVacancy] = useState('');
  const [experience, setExperience] = useState<ExpectedExperience>(ExpectedExperience.NO_EXPERIENCE);
  const [minSalary, setMinSalary] = useState<string>('0');
  const [maxSalary, setMaxSalary] = useState<string>('0');
  const dispatch = useAppDispatch();

  useEffect(() => {
    if (isStartRequestChangeVacancy === true && typeRequestModalVacancy === TypeRequestVacancyModal.CHANGE) {
      const vacancyBody: VacancyPutChangeParams = {
        name: nameVacancy,
        description: isEditorVacancyText,
        expected_experience: experience,
        salary_from: Number(minSalary),
        salary_to: Number(maxSalary),
        published: isPublishStatus
      };
      console.log(vacancyBody);
      if (vacancyByID) {
        dispatch(putVacancyChanges({idVacancy: vacancyByID.id, data: vacancyBody}))
          .then(() => {
            dispatch(getVacanciesForEmployer({isPublished: isPublishedVacancy, idDepartment: vacancyByID.department.id, offset: 0}))
              .then(() => {
                setIsOpenEditVacancy(false);
              });
          });
      }
      dispatch(setIsStartRequestChangeVacancy(false));
    }
  }, [isEditorVacancyText, isEditorVacancyFlag]);


  useEffect(() => {
    if (vacancyByID) {
      setNameVacancy(vacancyByID.name);
      if (vacancyByID?.salary_to) {
        vacancyByID?.salary_to !== 0 ? setMaxSalary(vacancyByID?.salary_to.toString()) : setMaxSalary('0');
      }
      if (vacancyByID?.salary_from) {
        vacancyByID?.salary_from !== 0 ? setMinSalary(vacancyByID?.salary_from.toString()) : setMinSalary('0');
      }
      if (vacancyByID?.expected_experience) {
        //setExperience(ExpectedExperience[vacancyByID?.expected_experience as ExpectedExperienceNameString]);
      }
    }
  }, [vacancyByID]);


  useEffect(() => {
    setIsOpenEditVacancy(isOpenEditVacancyModalState);
  }, [isOpenEditVacancyModalState]);

  useEffect(() => {
    dispatch(setIsOpenEditVacancyModal(isOpenEditVacancy));
  }, [isOpenEditVacancy]);

  const handleChangeNameVacancy = (e: ChangeEvent<HTMLInputElement>) => {
    setNameVacancy(e.target.value);
  };

  const onHandlerChangeExpectedExperience = (e: SingleValue<DepartmentsShortVersions>) => {
    if (e?.label) {
      const valueExp = Object.keys(ExpectedExperienceNameString).find(key => ExpectedExperienceNameString[key] === e.label);
      if (valueExp) {
        setExperience(valueExp);
      }
      console.log(e.label, valueExp);
    }
  };

  const handleChangeMinSalary = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.value) {
      setMinSalary(e.target.value.toString());
    }
  };

  const handleChangeMaxSalary = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.value) {
      setMaxSalary(e.target.value.toString());
    }
  };

  const putNewDescriptionVacancy = (e: any) => {
    //e.preventDefault();
    if (nameVacancy.length > 0 && !(Number(maxSalary) !== 0 && Number(maxSalary) <= Number(minSalary))) {
      dispatch(setIsEditorVacancyFlag());
    }
  };

  const handleUndoAction = (e: any) => {
    e.preventDefault();
    setIsOpenEditVacancy(false);
  };

  return (
    <Modal
      padding="80px 80px 60px 80px"
      width={1026}
      active={isOpenEditVacancy}
      setActive={setIsOpenEditVacancy}
    >
      <div className="edit-modal-item edit-modal-item__header">
        <div className="header header__title">Редактирование вакансии</div>
        <div className="header header__explanation">Заполните обязательные поля для редактирования вакансии</div>
      </div>
      <div className="edit-modal-item edit-modal-item__content">
        <div className="content-item">
          <div className="name-field">
            Статус вакансии*
          </div>
          <ModalBtnStatusVacancy isPublishStatus={isPublishStatus} setIsPublishStatus={setIsPublishStatus}/>
        </div>
        <div className="content-item">
          <div className="name-field">
            Название вакансии*
          </div>
          <input
            type="text"
            onChange={handleChangeNameVacancy}
            className="input-name-vacancy"
            value={nameVacancy}
          />
        </div>
        <div className="content-item">
          <div className="name-field">
            Опыт работы*
          </div>
          <Select
            className="basic-single"
            classNamePrefix="select"
            name=""
            options={expectedExperienceShortVersion}
            onChange={onHandlerChangeExpectedExperience}
            placeholder={ExpectedExperienceNameString[vacancyByID?.expected_experience as ExpectedExperience]}
          />
        </div>
        <div className="content-item">
          <div className="name-field">
            Зарплата
          </div>
          <div className="salaryInput-wrapper">
            <div className="text-field-salary text-field-salary__min">
              <input
                className="text-field-salary-input"
                type="number"
                min="0"
                value={minSalary}
                onChange={handleChangeMinSalary}
                placeholder="min"
              />
            </div>
            <div className="text-field-salary text-field-salary__max">
              <input
                className="text-field-salary-input"
                type="number"
                min="0"
                value={maxSalary}
                onChange={handleChangeMaxSalary}
                placeholder="max"
              />
            </div>
          </div>
        </div>
        <div className="content-item content-item__description">
          <div className="name-field">
            Описание вакансии*
          </div>
          <EmployerCreatingNewVacancy typeViewToolbar={TypeRequestVacancyModal.CHANGE}/>
        </div>
      </div>
      <div className="edit-modal-item edit-modal-item__nav">
        <GrayButton as="button" onClick={handleUndoAction}>Отмена</GrayButton>
        <BlueButton as="button"
                    className={cl({'disabledBlueBtn': nameVacancy.length <= 0 || (Number(maxSalary) !== 0 && Number(maxSalary) <= Number(minSalary))})}
                    onClick={putNewDescriptionVacancy}
        >
          Сохранить изменения
        </BlueButton>
      </div>
    </Modal>
  );
}

export default ModalEditVacancy;