import React, { Component } from 'react';
import FeatureListStore from '../stores/feature-list-store';

const FeatureListProvider = class extends Component {
    static displayName = 'FeatureListProvider'

    constructor(props, context) {
        super(props, context);
        this.state = {
            isSaving: FeatureListStore.isSaving,
            isLoading: FeatureListStore.isLoading,
            environmentFlags: FeatureListStore.getEnvironmentFlags(),
            projectFlags: FeatureListStore.getProjectFlags(),
            lastSaved: FeatureListStore.getLastSaved(),
            influxData: FeatureListStore.getFlagInfluxData(),
        };
        ES6Component(this);
        this.listenTo(FeatureListStore, 'change', () => {
            this.setState({
                isSaving: FeatureListStore.isSaving,
                isLoading: FeatureListStore.isLoading,
                environmentFlags: FeatureListStore.getEnvironmentFlags(),
                lastSaved: FeatureListStore.getLastSaved(),
                projectFlags: FeatureListStore.getProjectFlags(),
                influxData: FeatureListStore.getFlagInfluxData(),
            });
        });

        this.listenTo(FeatureListStore, 'saved', () => {
            this.props.onSave && this.props.onSave();
        });

        this.listenTo(FeatureListStore, 'problem', () => {
            this.setState({
                isSaving: FeatureListStore.isSaving,
                isLoading: FeatureListStore.isLoading,
                error: FeatureListStore.error,
                lastSaved: FeatureListStore.getLastSaved(),
                influxData: FeatureListStore.getFlagInfluxData(),
            });
            this.props.onError && this.props.onError(FeatureListStore.error);
        });
    }

    toggleFlag = (i, environments) => {
        AppActions.toggleFlag(i, environments);
    };

    setFlag = (i, flag, environments) => {
        AppActions.setFlag(i, flag, environments);
    };

    createFlag = (projectId, environmentId, flag, projectFlag, environmentFlag, segmentOverrides) => {
        AppActions.createFlag(projectId, environmentId, flag, segmentOverrides);
    };

    editFlag = (projectId, environmentId, flag, projectFlag, environmentFlag, segmentOverrides) => {
        AppActions.editFlag(projectId, Object.assign({}, projectFlag, flag), (newProjectFlag) => {
            AppActions.editEnvironmentFlag(projectId, environmentId, flag, projectFlag, {
                ...environmentFlag,
                multivariate_feature_state_values: newProjectFlag.multivariate_options && newProjectFlag.multivariate_options.map((v)=>({
                    multivariate_feature_option:v.id,
                    percentage_allocation:v.default_percentage_allocation
                }))
            }, segmentOverrides);
        });
    };

    removeFlag = (projectId, flag) => {
        AppActions.removeFlag(projectId, flag);
    };


    render() {
        return (
            this.props.children(
                {
                    ...this.state,
                },
                {
                    environmentHasFlag: FeatureListStore.hasFlagInEnvironment,
                    toggleFlag: this.toggleFlag,
                    setFlag: this.setFlag,
                    createFlag: this.createFlag,
                    editFlag: this.editFlag,
                    removeFlag: this.removeFlag,
                },
            )
        );
    }
};

FeatureListProvider.propTypes = {};

module.exports = FeatureListProvider;
