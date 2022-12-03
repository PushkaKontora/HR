import '../modal-edit-vacancy/modal-edit-vacancy.scss';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import React, {ChangeEvent, useEffect, useState} from 'react';
import {ExpectedExperience, ExpectedExperienceNameString, expectedExperienceShortVersion, SortingVacancyTypes, TypeRequestVacancyModal} from '../../const';
import {createVacancy, getVacanciesForEmployer} from '../../service/async-actions/async-actions-vacancy';
import {DepartmentsShortVersions, setIsEditorVacancyFlag, setIsOpenCreateVacancyModal, setIsStartRequestChangeVacancy} from '../../features/vacancy/vacancy-slice';
import Select, {SingleValue} from 'react-select';
import Modal from '../../reused-components/modal/modal';
import EmployerCreatingNewVacancy from '../employer-creating-new-vacancy/employer-creating-new-vacancy';
import {GrayButton} from '../styled/buttons/gray-button';
import {BlueButton} from '../styled/buttons/blue-button';
import {CreateVacancyParams} from '../../types/create-vacancy-params';
import ModalBtnStatusVacancy from '../modal-btn-status-vacancy/modal-btn-status-vacancy';

function ModalCreateVacancy() {
  const typeRequestModalVacancy = useAppSelector((state) => state.vacancy.typeRequestModalVacancy);
  const isPublishedVacancy = useAppSelector((state) => state.vacancy.isPublishedVacancy);
  const isOpenCreateVacancyModalFromRedux = useAppSelector((state) => state.vacancy.isOpenCreateVacancyModal);
  const isEditorVacancyText = useAppSelector((state) => state.vacancy.editorTextVacancy);
  const isEditorVacancyFlag = useAppSelector((state) => state.vacancy.isEditorVacancyFlag);
  const isStartRequestChangeVacancy = useAppSelector((state) => state.vacancy.isStartRequestChangeVacancy);
  const departmentID = useAppSelector((state) => state.general.user?.department.id);
  const [isOpenCreateVacancy, setIsOpenCreateVacancy] = useState(isOpenCreateVacancyModalFromRedux);
  const [isPublishStatus, setIsPublishStatus] = useState(isPublishedVacancy);
  const [nameVacancy, setNameVacancy] = useState('');
  const [experience, setExperience] = useState<ExpectedExperience>(ExpectedExperience.NO_EXPERIENCE);
  const [minSalary, setMinSalary] = useState<string>('0');
  const [maxSalary, setMaxSalary] = useState<string>('0');
  const dispatch = useAppDispatch();

  useEffect(() => {
    if (isStartRequestChangeVacancy === true
      && departmentID
      && typeRequestModalVacancy === TypeRequestVacancyModal.CREATE) {
      const vacancyBody: CreateVacancyParams = {
        name: nameVacancy,
        description: isEditorVacancyText,
        expected_experience: experience,
        salary_from: Number(minSalary),
        salary_to: Number(maxSalary),
        published: isPublishStatus,
        department_id: departmentID
      };
      console.log(vacancyBody);
      dispatch(createVacancy({data: vacancyBody}))
        .then(() => {
          dispatch(getVacanciesForEmployer({isPublished: isPublishedVacancy, idDepartment: departmentID, offset: 0}))
            .then(() => {
              setIsOpenCreateVacancy(false);
            });
        });

      dispatch(setIsStartRequestChangeVacancy(false));
    }
  }, [isEditorVacancyText, isEditorVacancyFlag]);


  useEffect(() => {
    setIsOpenCreateVacancy(isOpenCreateVacancyModalFromRedux);
  }, [isOpenCreateVacancyModalFromRedux]);

  useEffect(() => {
    dispatch(setIsOpenCreateVacancyModal(isOpenCreateVacancy));
  }, [isOpenCreateVacancy]);

  const handleChangeNameVacancy = (e: ChangeEvent<HTMLInputElement>) => {
    setNameVacancy(e.target.value);
  };

  const onHandlerChangeExpectedExperience = (e: SingleValue<DepartmentsShortVersions>) => {
    if (e?.label) {
      const valueExp = Object.keys(ExpectedExperienceNameString).find((key) => ExpectedExperienceNameString[key] === e.label);
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

  const handlerClickCreateVacancy = (e: any) => {
    if (nameVacancy.length > 0 && !(Number(maxSalary) !== 0 && Number(maxSalary) <= Number(minSalary))) {
      dispatch(setIsEditorVacancyFlag());
    }
    //e.preventDefault();
  };

  const handleUndoAction = (e: any) => {
    e.preventDefault();
    setIsOpenCreateVacancy(false);
  };

  return (
    <Modal
      padding="80px 80px 60px 80px"
      width={1026}
      active={isOpenCreateVacancy}
      setActive={setIsOpenCreateVacancy}
    >
      <div className="edit-modal-item edit-modal-item__header">
        <div className="header header__title">Создание новой вакансии</div>
        <div className="header header__explanation">Заполните обязательные поля для создания вакансии</div>
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
            placeholder="Введите название"
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
            placeholder={ExpectedExperienceNameString[experience as ExpectedExperience]}
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
          <EmployerCreatingNewVacancy typeViewToolbar={TypeRequestVacancyModal.CREATE}/>
        </div>
      </div>
      <div className="edit-modal-item edit-modal-item__nav">
        <GrayButton as="button" onClick={handleUndoAction}>Отмена</GrayButton>
        <BlueButton as="button" onClick={handlerClickCreateVacancy}>
          Создать вакансию
        </BlueButton>
      </div>
    </Modal>
  );
}

export default ModalCreateVacancy;