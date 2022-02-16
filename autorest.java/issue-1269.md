## Reference
Scenario tests definition:
https://github.com/Azure/azure-rest-api-specs/blob/main/documentation/api-scenario/references/ApiScenarioDefinition.md

## plan

### Phase 1
 * Support simple test-modeler code model in CodeModel
 * Support code generation on new CodeModel
   * support `RestCall` step type with `exampleFile`

plan: 
 * simple parameter parse
 * CodeModel definition
 * Preprocessor process
 * Test model to Client scenario model
 * scenario model generation ( similar to sample generation )

#### Design: 
 * mapping
   * `scenarioTests` to `LiveTests` (A unit test java file with multiple test cases)
   * `scenario` to `LiveTestCase` (test cases within `LiveTests` file)
 * implementation
   * add method in `ExampleParser` to parse examples in scenario tests into `LiveTests`
   * add an additional `FluentLiveTestsTemplate` to write `LiveTests` into java file

### Phase 2
 * Support `RestOperations` step type with `ResourceUpdate` etc.
 * Support armTemplate?
