/*
Seed to enrich existing story presets with hierarchy controls.
Merge these fields into the current steps.
The defaults below are chosen to reduce clutter, especially on thesis structure steps.
*/

export const STORY_PRESET_OVERRIDES = {
  'structure-these': {
    defaultStepOptions: {
      edgeMode: 'strict',
      includeNeighbors: false,
      secondaryDepth: 0,
      hideBackbone: true,
      fitTargets: 'primary',
      backboneRelationTypes: ['partOf', 'source', 'citedIn', 'relatedTo']
    },
    steps: {
      s1: {
        hideRelationTypes: ['partOf', 'source', 'citedIn', 'relatedTo']
      },
      s2: {
        hideRelationTypes: ['partOf', 'source', 'citedIn', 'relatedTo']
      },
      s3: {
        edgeMode: 'neighbors',
        includeNeighbors: true,
        secondaryDepth: 1,
        maxSecondaryPerTarget: 4,
        hideBackbone: true,
        fitTargets: 'primary+secondary'
      },
      s4: {
        hideRelationTypes: ['partOf', 'source', 'citedIn', 'relatedTo']
      }
    }
  },

  'monetisation-cryptos': {
    defaultStepOptions: {
      edgeMode: 'strict',
      includeNeighbors: false,
      secondaryDepth: 0,
      hideBackbone: true,
      fitTargets: 'primary'
    },
    steps: {
      m3: {
        edgeMode: 'neighbors',
        includeNeighbors: true,
        secondaryDepth: 1,
        maxSecondaryPerTarget: 3,
        fitTargets: 'primary+secondary'
      },
      m4: {
        edgeMode: 'neighbors',
        includeNeighbors: true,
        secondaryDepth: 1,
        maxSecondaryPerTarget: 3,
        fitTargets: 'primary+secondary'
      },
      m5: {
        edgeMode: 'neighbors',
        includeNeighbors: true,
        secondaryDepth: 1,
        maxSecondaryPerTarget: 4,
        hideBackbone: true,
        fitTargets: 'primary+secondary'
      }
    }
  },

  'qui-gouverne-reellement': {
    defaultStepOptions: {
      edgeMode: 'neighbors',
      includeNeighbors: true,
      secondaryDepth: 1,
      maxSecondaryPerTarget: 4,
      hideBackbone: true,
      fitTargets: 'primary+secondary'
    },
    steps: {
      q1: {
        edgeMode: 'strict',
        includeNeighbors: false,
        fitTargets: 'primary'
      },
      q2: {
        hideRelationTypes: ['partOf', 'source']
      },
      q3: {
        hideRelationTypes: ['partOf', 'source', 'citedIn']
      },
      q4: {
        edgeMode: 'strict',
        includeNeighbors: false,
        fitTargets: 'primary'
      }
    }
  },

  'crises': {
    defaultStepOptions: {
      edgeMode: 'strict',
      includeNeighbors: false,
      secondaryDepth: 0,
      hideBackbone: true,
      fitTargets: 'primary'
    },
    steps: {
      c2: {
        edgeMode: 'neighbors',
        includeNeighbors: true,
        secondaryDepth: 1,
        maxSecondaryPerTarget: 3,
        fitTargets: 'primary+secondary'
      },
      c3: {
        edgeMode: 'neighbors',
        includeNeighbors: true,
        secondaryDepth: 1,
        maxSecondaryPerTarget: 4,
        fitTargets: 'primary+secondary'
      },
      c4: {
        edgeMode: 'strict',
        includeNeighbors: false,
        fitTargets: 'primary'
      }
    }
  }
};
