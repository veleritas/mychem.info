import biothings.hub.dataload.uploader as uploader

class AeolusUploader(uploader.DummySourceUploader):

    name = "aeolus"
    __metadata__ = {
            "src_meta" : {
                "url" : "http://www.nature.com/articles/sdata201626",
                "license_url" : "http://datadryad.org/resource/doi:10.5061/dryad.8q0s4",
		"license_url_short" : "https://goo.gl/pLRNT8",
                "license" : "CC0 1.0",
                }
            }

    @classmethod
    def get_mapping(klass):
        mapping = {
            "aeolus": {
                "properties": {
                    "drug_id": {
                        "type": "string",
                        "analyzer": "string_lowercase"
                    },
                    "drug_name": {
                        "type": "string",
                    },
                    "inchikey": {
                        "type": "string",
                        "analyzer": "string_lowercase"
                    },
                    "no_of_outcomes": {
                        "type": "integer",
                    },
                    "pt": {
                        "type": "string",
                    },
                    "unii": {
                        "type": "string",
                        "analyzer": "string_lowercase"
                    },
					"drug_vocab": {
						"type": "string"
					},
                    "drug_code": {
                        "analyzer": "string_lowercase",
                        "type": "string"
                    },
					"rxcui": {
						"analyzer": "string_lowercase",
						"type": "string"
					},
					"relationships": {
						"properties": {
							"relatedSubstance": {
								"properties": {
									"approvalID": {
										"analyzer": "string_lowercase",
										"type": "string"
										},
									"refPname": {
										"analyzer": "string_lowercase",
										"type": "string"
										}
									}
								},
							"type": {
								"analyzer": "string_lowercase",
								"type": "string"
								}
							}
						},
                    "outcomes": {
                        "properties": {
							"code": {
								"analyzer": "string_lowercase",
								"type": "string"
								},
							"vocab": {
								"include_in_all": False,
								"type": "string"
								},
                            "case_count": {
                                "type": "long",
                            },
                            "id": {
                                "type": "string",
                                "analyzer": "string_lowercase"
                            },
                            "name": {
                                "type": "string",
                            },
                            "prr": {
                                "type": "float",
                            },
                            "prr_95_ci": {
                                "type": "float",
                            },
                            "ror": {
                                "type": "float",
                            },
                            "ror_95_ci": {
                                "type": "float",
                            },
                        },
                    }
                }
            }
        }

        return mapping
