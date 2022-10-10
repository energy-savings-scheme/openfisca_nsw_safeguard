from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np
import datetime
import time
from datetime import datetime as py_datetime
from datetime import date


class PDRS__can_create_PDRS_certificate(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Can you create the PDRS certificate?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PDRS Can Create Certificate",
        # "major-cat":"Peak Demand Reduction Scheme",
        # "monor-cat":'General Requirements'
    }

    def formula(buildings, period, parameters):
        have_implemented_PDR_activity = buildings('PDRS__have_implemented_PDR_activity', period)
        have_accreditation = buildings('PDRS__have_accreditation', period)
        implementation_after_1_July_2022 = buildings('PDRS__implementation_after_1_April_2022', period)
        certificates_have_been_calculated = buildings('PDRS__certificates_have_been_calculated', period)
        application_during_transition_period = buildings('PDRS__application_during_transition_period', period)
        is_IPART_approved_accreditation = buildings('PDRS__is_IPART_approved_accreditation', period)
        certificate_already_been_created_during_compliance_period = buildings('PDRS__certificate_already_been_created_during_compliance_period', period)
        have_provided_required_data_and_evidence = buildings('PDRS__have_provided_required_data_and_evidence', period)
        used_administrator_registry = buildings('PDRS__used_administrator_registry', period)
        registration_date_before_30_Sept = buildings('PDRS__registration_date_before_30_Sept', period)

        is_eligible = (
          have_implemented_PDR_activity *
          have_accreditation *
          implementation_after_1_July_2022 * 
          certificates_have_been_calculated *
          application_during_transition_period * 
          is_IPART_approved_accreditation * 
          certificate_already_been_created_during_compliance_period * 
          have_provided_required_data_and_evidence *
          used_administrator_registry * 
          registration_date_before_30_Sept
        )

        return is_eligible


class PDRS__have_implemented_PDR_activity(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Has implementation already occurred?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PDRS Have Implemented PDR Activity",
        # "major-cat":"Peak Demand Reduction Scheme",
        # "monor-cat":'General Requirements',
    }


class PDRS__have_accreditation(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Do you have an accreditation for the PDRS activity?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PDRS Have Implemented PDR Activity",
        # "major-cat":"Peak Demand Reduction Scheme",
        # "monor-cat":'General Requirements'
    }


class PDRS__implementation_after_1_April_2022(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Is the implementation after 1 April 2022?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PDRS Have Implemented PDR Activity",
        # "major-cat":"Peak Demand Reduction Scheme",
        # "monor-cat":'General Requirements'
    }


class PDRS__certificates_have_been_calculated(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Have PDRS certificates been created?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PDRS Certificates Been Created",
        # "major-cat":"Peak Demand Reduction Scheme",
        # "monor-cat":'General Requirements'
    }


class PDRS__application_during_transition_period(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the application to create certificates during the Transition Period?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PDRS Application during Transition Period",
        # "major-cat":"Peak Demand Reduction Scheme",
        # "monor-cat":'General Requirements'
    }


class PDRS__is_IPART_approved_accreditation(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the accreditation approved by IPART?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PDRS Have Implemented PDR Activity",
        # "major-cat":"Peak Demand Reduction Scheme",
        # "monor-cat":'General Requirements'
    }


class PDRS__certificate_already_been_created_during_compliance_period(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Have certificates already been created for these demand savings within the compliance period?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PDRS Certificates Already Created",
        # "major-cat":"Peak Demand Reduction Scheme",
        # "monor-cat":'General Requirements'
    }


class PDRS__have_provided_required_data_and_evidence(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the required data and evidence been provided?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PDRS Required Data and Evidence Has Been Provided",
        # "major-cat":"Peak Demand Reduction Scheme",
        # "monor-cat":'General Requirements'
    }


class PDRS__used_administrator_registry(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the Administrator registry been used to register the certificate?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PDRS Administrator Registry Has Been Used",
        # "major-cat":"Peak Demand Reduction Scheme",
        # "monor-cat":'General Requirements'
    }


class PDRS__registration_date_before_30_Sept(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the Registration Date before 30 September?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PDRS Registration Date before 30 September",
        # "major-cat":"Peak Demand Reduction Scheme",
        # "monor-cat":'General Requirements'
    }


class PDRS__testing_evidence_is_required(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is testing evidence required for the PDRS Activity?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PDRS Testing Evidence is Required",
        # "major-cat":"Peak Demand Reduction Scheme",
        # "monor-cat":'General Requirements'
    }
