import Utils from '../../utils/utils';

module.exports = (envId, { FEATURE_NAME, FEATURE_FUNCTION, FEATURE_NAME_ALT }) => `use BulletTrain\\BulletTrain;

$bt = new BulletTrain('${envId}');

// Check for a feature
$${FEATURE_NAME} = $bt->featureEnabled("${FEATURE_NAME}");

// Or, use the value of a feature
$${FEATURE_NAME_ALT} = $bt->getValue("${FEATURE_NAME_ALT}");
`;
